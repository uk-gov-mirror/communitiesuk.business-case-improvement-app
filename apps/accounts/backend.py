from django.contrib.auth.backends import ModelBackend

from .authentication import Authentication


class EntraBackend(ModelBackend):
    """
    Only kicks in when called with `token=...` (see views.entra_callback).
    A plain `authenticate(request, username=..., password=...)` call —
    e.g. against the Django admin login form — falls through to
    ModelBackend's own behaviour untouched, which is what lets
    superusers keep using a password even when Entra is enabled.
    """

    def authenticate(self, request, token=None, *args, **kwargs):
        if not token:
            return None

        user = Authentication(request).authenticate(token)
        if self.user_can_authenticate(user):
            return user
        return None
