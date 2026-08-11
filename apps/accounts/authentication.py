import datetime
import logging
from http import HTTPStatus
from typing import Optional
from urllib import parse

import msal
import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError, transaction
from django.http import HttpRequest

from .exceptions import EntraAuthException, FlowError, TokenError
from .models import User

logger = logging.getLogger(__name__)


class Authentication:
    """
    Wraps `msal.ConfidentialClientApplication` to run the OAuth2
    authorization-code flow against Entra ID, and maps the resulting
    claims/profile onto a Django `User`.

    One instance is created per-request; the MSAL token cache and the
    in-flight auth flow both live in the Django session, so there's no
    server-side state to manage beyond that.
    """

    def __init__(self, request: HttpRequest):
        self.request = request
        self.graph_user_endpoint = settings.ENTRA_AUTH.get(
            "GRAPH_USER_ENDPOINT", "https://graph.microsoft.com/v1.0/me"
        )
        self.auth_flow_session_key = "auth_flow"
        self._cache = msal.SerializableTokenCache()
        self._msal_app = None

        # Eagerly load claims already stashed in the session from a
        # previous request in this session (used by `user_is_authenticated`).
        self.claims = self.request.session.get("id_token_claims", {})

    #  Login: step 1 (redirect to Entra)

    def get_auth_uri(self, state: Optional[str] = None) -> str:
        redirect_uri = self._get_redirect_uri()
        flow = self.msal_app.initiate_auth_code_flow(
            scopes=settings.ENTRA_AUTH["SCOPES"],
            redirect_uri=redirect_uri,
            state=state,
        )
        self.request.session[self.auth_flow_session_key] = flow
        return flow["auth_uri"]

    # Login: step 2 (Entra redirects back to Business Case App callback)

    def get_token_from_flow(self):
        flow = self.request.session.pop(self.auth_flow_session_key, {})
        if not flow:
            raise FlowError("Auth flow could not be found in the session.")

        token = self.msal_app.acquire_token_by_auth_code_flow(
            auth_code_flow=flow, auth_response=self.request.GET
        )
        if "error" in token:
            raise TokenError(token.get("error"), token.get("error_description"))

        self._save_cache()
        self.request.session["id_token_claims"] = token["id_token_claims"]
        return token

    def get_token_from_cache(self, username: Optional[str] = None):
        accounts = self.msal_app.get_accounts(username)
        if not accounts:
            return None

        token_result = self.msal_app.acquire_token_silent(
            scopes=settings.ENTRA_AUTH["SCOPES"], account=accounts[0]
        )
        self._save_cache()

        # acquire_token_silent doesn't always return id_token_claims:
        # https://github.com/AzureAD/microsoft-authentication-library-for-python/issues/139
        if token_result and token_result.get("id_token_claims"):
            self.request.session["id_token_claims"] = token_result["id_token_claims"]
        return token_result

    #  Claims/profile -> Django user

    def authenticate(self, token: dict):
        user_profile = self._get_user_profile(token["access_token"])

        # https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference
        attributes = {**user_profile, **token.get("id_token_claims", {})}

        if not self._is_tenant_allowed(attributes):
            logger.warning(
                "Login rejected: tenant %s not in allow-list", attributes.get("tid")
            )
            return AnonymousUser()

        try:
            return self._get_or_create_user(**attributes)
        except IntegrityError:
            logger.warning(
                "Could not attach Entra identity oid=%s tid=%s to a user account",
                attributes.get("oid"),
                attributes.get("tid"),
            )
            return AnonymousUser()

    #  Logout

    def get_logout_uri(self) -> str:
        query_params = {
            "post_logout_redirect_uri": settings.ENTRA_AUTH.get("LOGOUT_REDIRECT"),
            "logout_hint": self.claims.get("login_hint"),
        }
        query_params = {k: v for k, v in query_params.items() if v}
        return (
            f"{settings.ENTRA_AUTH['AUTHORITY']}/oauth2/v2.0/logout?"
            f"{parse.urlencode(query_params)}"
        )

    #  Check Session Info. Is Session still valid?

    @property
    def user_is_authenticated(self) -> bool:
        if not self.request.user.is_authenticated:
            return False

        # Superusers created via `createsuperuser` may have no Entra TODO: Check this
        if isinstance(self.request.user, User) and self.request.user.is_superuser:
            return True

        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if now < self.claims.get("exp", 0):
            return True

        # ID token has expired — try a silent refresh before giving up.
        return self.get_token_from_cache(self.request.user.get_username()) is not None

    @property
    def msal_app(self):
        if self._msal_app is None:
            self._msal_app = msal.ConfidentialClientApplication(
                client_id=settings.ENTRA_AUTH["CLIENT_ID"],
                client_credential=settings.ENTRA_AUTH["CLIENT_SECRET"],
                authority=settings.ENTRA_AUTH["AUTHORITY"],
                token_cache=self.cache,
            )
        return self._msal_app

    @property
    def cache(self):
        if self.request.session.get("token_cache"):
            self._cache.deserialize(self.request.session["token_cache"])
        return self._cache

    def _save_cache(self):
        if self.cache.has_state_changed:
            self.request.session["token_cache"] = self.cache.serialize()

    def _get_redirect_uri(self) -> str:
        redirect_uri = settings.ENTRA_AUTH["REDIRECT_URI"]
        if not redirect_uri.startswith("http"):
            redirect_uri = self.request.build_absolute_uri(redirect_uri)
        return redirect_uri

    def _get_user_profile(self, access_token: str) -> dict:
        response = requests.get(
            self.graph_user_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        if response.ok:
            return response.json()

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            error = response.json().get("error", {})
            raise TokenError(error.get("code"), error.get("message"))

        raise EntraAuthException("An error occurred while contacting the Graph API.")

    def _is_tenant_allowed(self, attributes: dict) -> bool:
        return attributes.get("tid") in settings.ENTRA_AUTH.get("ALLOWED_TENANTS", [])

    # -- User provisioning

    def _get_or_create_user(self, **attributes):
        user = self._find_user(**attributes)
        if user:
            self._update_user(user, **attributes)
            return user

        # No usable password: Entra users authenticate against Microsoft,
        # never against a locally-stored password.
        with transaction.atomic():
            user = User.objects.create_user(**self._user_mapping(**attributes))
            user.set_unusable_password()
            user.save(update_fields=["password"])
            return user

    def _find_user(self, **attributes):
        mapping = self._user_mapping(**attributes)
        return self._find_user_by_entra_identity(mapping) or self._find_unlinked_user(
            mapping
        )

    def _find_user_by_entra_identity(self, mapping):
        return User.objects.filter(
            entra_oid=mapping["entra_oid"], entra_tid=mapping["entra_tid"]
        ).first()

    def _find_unlinked_user(self, mapping):
        """
        Lets you pre-provision users (e.g. via the admin, to assign roles
        ahead of time) who get linked to their Entra identity automatically
        the first time they sign in. - For first time use, or for setting up
        test users before they login - useful for Authorisation in the future
        """
        unlinked = User.objects.filter(entra_oid__isnull=True, entra_tid__isnull=True)
        return (
            unlinked.filter(email__iexact=mapping["email"]).first()
            or unlinked.filter(username__iexact=mapping["username"]).first()
        )

    def _update_user(self, user, **attributes):
        for field, value in self._user_mapping(**attributes).items():
            setattr(user, field, value)
        user.save()

    def _user_mapping(self, **attributes) -> dict:
        return {
            "first_name": attributes.get("givenName", ""),
            "last_name": attributes.get("surname", ""),
            "email": attributes["mail"],
            "username": attributes["preferred_username"],
            "entra_oid": attributes["oid"],
            "entra_tid": attributes["tid"],
        }
