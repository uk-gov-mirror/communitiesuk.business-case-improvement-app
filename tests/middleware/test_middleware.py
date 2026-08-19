"""
These tests require ENTRA_ID_ENABLED=True at Django startup - set in Env file/terminal
"""

from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from apps.accounts.middleware import EntraMiddleware
from apps.accounts.models import User


def make_middleware(response_marker="downstream response"):
    calls = []

    def get_response(request):
        calls.append(request)
        return response_marker

    middleware = EntraMiddleware(get_response)
    return middleware, calls


def make_request(path):
    request = RequestFactory().get(path)
    request.user = AnonymousUser()
    request.session = {}
    return request


def test_health_path_bypasses_auth_entirely():
    middleware, calls = make_middleware()
    request = make_request("/health")

    result = middleware(request)

    assert result == "downstream response"
    assert len(calls) == 1


def test_admin_login_is_not_public():
    middleware, calls = make_middleware()
    request = make_request("/admin/login/")

    result = middleware(request)

    assert len(calls) == 0
    assert result.status_code == 302
    assert result.url.startswith(reverse("accounts:login"))


def test_login_route_itself_is_public():
    middleware, calls = make_middleware()
    request = make_request(reverse("accounts:login"))

    result = middleware(request)

    assert result == "downstream response"
    assert len(calls) == 1


def test_unauthenticated_request_redirects_to_login_with_next():
    middleware, calls = make_middleware()
    request = make_request("/some/protected/page")

    result = middleware(request)

    assert len(calls) == 0
    assert result.status_code == 302
    assert "next=/some/protected/page" in result.url


@pytest.mark.django_db
def test_authenticated_superuser_is_not_blocked():
    middleware, calls = make_middleware()
    user = User.objects.create_user(
        username="admin", email="admin@example.gov.uk", is_superuser=True, is_staff=True
    )
    request = make_request("/admin/")
    request.user = user

    with patch(
        "apps.accounts.middleware.Authentication.user_is_authenticated",
        new_callable=lambda: property(lambda self: True),
    ):
        result = middleware(request)

    assert result == "downstream response"
    assert len(calls) == 1


@pytest.mark.django_db
def test_expired_session_redirects_even_for_a_previously_valid_user():
    middleware, calls = make_middleware()
    user = User.objects.create_user(username="alice", email="alice@example.gov.uk")
    request = make_request("/some/page")
    request.user = user

    with patch(
        "apps.accounts.middleware.Authentication.user_is_authenticated",
        new_callable=lambda: property(lambda self: False),
    ):
        result = middleware(request)

    assert len(calls) == 0
    assert result.status_code == 302
