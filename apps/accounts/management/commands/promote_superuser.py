from django.core.management.base import BaseCommand, CommandError

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
            required=True,
            help="Email address matching the person's Entra account.",
        )

    def handle(self, *args, **options):
        email = options["email"].strip().lower()
        if not email:
            raise CommandError("--email must not be empty")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email},
        )

        if user.entra_oid:
            self.stdout.write(
                self.style.WARNING(
                    f"{email} is already linked to an Entra identity "
                    f"(oid={user.entra_oid}); promoting in place."
                )
            )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if created:
            user.set_unusable_password()
        user.save()

        action = "Created and promoted" if created else "Promoted existing user"
        self.stdout.write(self.style.SUCCESS(f"{action}: {email}"))
        self.stdout.write(
            "They will get superuser access the next time they sign in via Entra."
        )
