import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .authentication import Authentication
from .exceptions import FlowError
from .utils import EntraStateSerializer

serializer = EntraStateSerializer()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Entra flow — used when settings.ENTRA_ID_ENABLED is True (test/prod)
# ---------------------------------------------------------------------------


@login_not_required
def entra_login(request: HttpRequest):
    redirect_url = Authentication(request).get_auth_uri(
        state=serializer.serialize(next=request.GET.get("next"))
    )
    return HttpResponseRedirect(redirect_url)


@login_not_required
def entra_logout(request: HttpRequest):
    authentication = Authentication(request)
    logout(request)
    return HttpResponseRedirect(authentication.get_logout_uri())


@login_not_required
def entra_callback(request: HttpRequest):
    try:
        token = Authentication(request).get_token_from_flow()
    except FlowError as error:
        logger.error(error)
        request.session.flush()
        raise PermissionDenied(
            "Unable to complete the authentication process."
        ) from error

    user = authenticate(request, token=token)
    if not user:
        raise PermissionDenied("You are not allowed to access this application.")

    login(request, user)

    next_url = settings.LOGIN_REDIRECT_URL
    if state := request.GET.get("state"):
        candidate = serializer.deserialize(state).get("next")
        if candidate and url_has_allowed_host_and_scheme(
            candidate,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = candidate

    return HttpResponseRedirect(next_url)


# ---------------------------------------------------------------------------
# Dev-only password login — used when settings.ENTRA_ID_ENABLED is False
# ---------------------------------------------------------------------------


@login_not_required
def dev_login(request: HttpRequest):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return redirect(next_url)
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(
        request,
        "accounts/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@login_not_required
def dev_logout(request: HttpRequest):
    logout(request)
    return redirect("accounts:login")
