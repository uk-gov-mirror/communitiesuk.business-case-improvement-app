import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.accounts.models import User


@pytest.mark.django_db
def test_creates_unlinked_superuser_by_email():
    call_command("promote_superuser", "--email", "admin@example.gov.uk")

    user = User.objects.get(email="admin@example.gov.uk")
    assert user.is_superuser is True
    assert user.is_staff is True
    assert user.entra_oid is None
    assert user.entra_tid is None
    assert user.has_usable_password() is False


@pytest.mark.django_db
def test_promotes_an_existing_linked_user_in_place():
    """Covers running the command against someone who has already signed
    in at least once — get_or_create must find, not duplicate, them."""
    existing = User.objects.create_user(
        username="alice@example.gov.uk",
        email="alice@example.gov.uk",
        entra_oid="11111111-1111-1111-1111-111111111111",
        entra_tid="22222222-2222-2222-2222-222222222222",
    )
    assert existing.is_superuser is False

    call_command("promote_superuser", "--email", "alice@example.gov.uk")

    existing.refresh_from_db()
    assert existing.is_superuser is True
    assert existing.is_staff is True
    assert (
        str(existing.entra_oid) == "11111111-1111-1111-1111-111111111111"
    )  # untouched
    assert User.objects.count() == 1  # no duplicate row


@pytest.mark.django_db
def test_is_idempotent():
    call_command("promote_superuser", "--email", "admin@example.gov.uk")
    call_command("promote_superuser", "--email", "admin@example.gov.uk")

    assert User.objects.filter(email="admin@example.gov.uk").count() == 1


@pytest.mark.django_db
def test_falls_back_to_settings_when_no_email_flag_given(settings):
    settings.ENTRA_AUTH = {"BOOTSTRAP_ADMIN_EMAIL": "fallback@example.gov.uk"}

    call_command("promote_superuser")

    assert User.objects.filter(
        email="fallback@example.gov.uk", is_superuser=True
    ).exists()


@pytest.mark.django_db
def test_raises_without_email_from_either_source(settings):
    settings.ENTRA_AUTH = {}

    with pytest.raises(CommandError):
        call_command("promote_superuser")


@pytest.mark.django_db
def test_matches_existing_user_case_insensitively():
    existing = User.objects.create_user(
        username="Richard.Byrne@communities.gov.uk",
        email="Richard.Byrne@communities.gov.uk",
        entra_oid="11111111-1111-1111-1111-111111111111",
        entra_tid="22222222-2222-2222-2222-222222222222",
    )

    call_command("promote_superuser", "--email", "richard.byrne@communities.gov.uk")

    existing.refresh_from_db()
    assert existing.is_superuser is True
    assert existing.is_staff is True
    assert User.objects.count() == 1  # no duplicate row created
