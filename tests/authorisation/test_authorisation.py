import time

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User


def authenticated_client(user):
    client = Client()
    client.force_login(user)
    session = client.session
    session["id_token_claims"] = {"exp": time.time() + 3600}
    session.save()
    return client


@pytest.mark.django_db
def test_regular_authenticated_user_cannot_reach_admin_dashboard():
    user = User.objects.create_user(username="foo", email="foo@example.gov.uk")
    client = authenticated_client(user)

    resp = client.get("/admin/")

    assert resp.status_code == 302
    assert resp["Location"] == "/"


@pytest.mark.django_db
def test_superuser_can_reach_admin_dashboard():
    user = User.objects.create_user(
        username="admin", email="admin@example.gov.uk", is_superuser=True, is_staff=True
    )
    client = authenticated_client(user)

    resp = client.get("/admin/")

    assert resp.status_code == 200
    assert b"Site administration" in resp.content


@pytest.mark.django_db
def test_admin_login_route_never_renders_a_password_form():
    anonymous_client = Client()

    resp = anonymous_client.get("/admin/login/")

    assert resp.status_code == 302
    assert resp["Location"].startswith(reverse("accounts:login"))


@pytest.mark.django_db
def test_admin_login_route_unreachable_even_for_an_authenticated_regular_user():
    user = User.objects.create_user(username="alice", email="alice@example.gov.uk")
    client = authenticated_client(user)

    resp = client.get("/admin/login/")

    assert resp.status_code == 302
    assert resp["Location"] == "/"
