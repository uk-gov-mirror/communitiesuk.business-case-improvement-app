from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from .authentication import Authentication

ADMIN_PATH_PREFIX = "/admin/"  # block access to /admin for non admins


class EntraMiddleware:
    """
    Only registered when ENTRA_ID_ENABLED is True (see config/settings.py).
    In dev, Django's own LoginRequiredMiddleware is used instead,
    """

    def __init__(self, get_response):
        self.get_response = get_response
        public_views = ["accounts:login", "accounts:logout", "accounts:callback"]
        public_views.extend(settings.ENTRA_AUTH.get("PUBLIC_URLS", []))
        # Strip trailing / if registered with this in Entra (which we do not directly manage)
        # this resolves e.g /auth_callback/ and /auth_callback
        self.public_urls = {
            reverse(view_name).rstrip("/") for view_name in public_views
        }
        self.public_paths = ["/health"] + settings.ENTRA_AUTH.get("PUBLIC_PATHS", [])

    def __call__(self, request: HttpRequest):
        if request.path_info.rstrip("/") in self.public_urls:
            return self.get_response(request)

        for path in self.public_paths:
            if request.path_info.startswith(path):
                return self.get_response(request)

        # Check if authenticated
        if not Authentication(request).user_is_authenticated:
            return redirect(
                f"{reverse('accounts:login')}?next={urlparse(request.path).path}"
            )

        # Block users accessing the /admin page if they are not active or staff
        if request.path_info.startswith(ADMIN_PATH_PREFIX):
            if not (request.user.is_active and request.user.is_staff):
                return redirect("/")

        return self.get_response(request)
