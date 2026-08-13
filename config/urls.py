"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from apps.triage import views as triage_views
from apps.accounts import views as accounts_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("triage/", include("apps.triage.urls", namespace="triage")),
    path("", triage_views.index, name="index"),  # home route
]

if settings.ENTRA_ID_ENABLED:
    # Use configured Entra Callback Env var
    # allows different values for e.g Localhost and AWS
    from urllib.parse import urlparse

    _callback_path = urlparse(settings.ENTRA_AUTH["REDIRECT_URI"]).path.lstrip("/")
    urlpatterns.insert(
        0,
        path(_callback_path, accounts_views.entra_callback, name="auth_callback"),
    )
