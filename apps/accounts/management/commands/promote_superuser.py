from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from apps.accounts.models import User


class Command(BaseCommand):
    """
    Creates (or promotes an existing) user to superuser/staff status by
    email, without setting a password.

    Safe to run more than once — it's idempotent.

    Usage:
        python manage.py promote_superuser --email <user_email>
    """

    help = "Create or promote a user to superuser/staff status by email (Entra mode)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=False,
            help="Email address matching the person's Entra account.",
        )

    def handle(self, *args, **options):
        email = (
            options.get("email")
            or settings.ENTRA_AUTH.get("BOOTSTRAP_ADMIN_EMAIL")
            or ""
        ).strip()

        if not email:
            raise CommandError(
                "No email provided. Pass --email, or set ENTRA_BOOTSTRAP_ADMIN_EMAIL."
            )

        # Match case-insensitively. Entra's Graph API commonly returns `mail`
        # in mixed case ("Firstname.Lastname@example_org.gov.uk"), and that is what
        # gets stored when a user is provisioned on first sign-in. A mis match would create a *second*
        # account holding the superuser flags, leaving the real signed-in
        # user without admin access.
        user = User.objects.filter(email__iexact=email).first()
        created = user is None

        if created:
            user = User.objects.create_user(email=email, username=email)
            user.set_unusable_password()
        elif user.entra_oid:
            self.stdout.write(
                self.style.WARNING(
                    f"{user.email} is already linked to an Entra identity "
                    f"(oid={user.entra_oid}); promoting in place."
                )
            )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        action = "Created and promoted" if created else "Promoted existing user"
        self.stdout.write(self.style.SUCCESS(f"{action}: {user.email}"))
        self.stdout.write(
            "They will get superuser access the next time they sign in via Entra."
        )
