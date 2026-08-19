from django.conf import settings
from django.urls import path

from . import views

app_name = "accounts"

if settings.ENTRA_ID_ENABLED:
    urlpatterns = [
        path("login/", views.entra_login, name="login"),
        path("logout/", views.entra_logout, name="logout"),
    ]
else:
    # Dev only: plain Django username/password auth, no Entra involved.
    urlpatterns = [
        path("login/", views.dev_login, name="login"),
        path("logout/", views.dev_logout, name="logout"),
    ]
