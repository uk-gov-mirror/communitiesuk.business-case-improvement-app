from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from .authentication import Authentication


class EntraMiddleware:
    """
    Only registered when ENTRA_ID_ENABLED is True (see config/settings.py).
    In dev, Django's own LoginRequiredMiddleware is used instead,
    """

    def __init__(self, get_response):
        self.get_response = get_response
        public_views = ["accounts:login", "accounts:logout", "accounts:callback"]
        public_views.extend(settings.ENTRA_AUTH.get("PUBLIC_URLS", []))
        self.public_urls = [reverse(view_name) for view_name in public_views]
        self.public_paths = ["/health"] + settings.ENTRA_AUTH.get("PUBLIC_PATHS", [])

    def __call__(self, request: HttpRequest):
        if request.path_info in self.public_urls:
            return self.get_response(request)

        for path in self.public_paths:
            if request.path_info.startswith(path):
                return self.get_response(request)

        if Authentication(request).user_is_authenticated:
            return self.get_response(request)

        return redirect(
            f"{reverse('accounts:login')}?next={urlparse(request.path).path}"
        )
