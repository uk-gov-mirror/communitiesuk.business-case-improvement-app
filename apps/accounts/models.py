from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model, replacing django.contrib.auth.models.User before
    the first migration is run.

    - In dev (ENTRA_ID_ENABLED=False): plain username/password auth via
      ModelBackend. Create accounts with `manage.py createsuperuser`.
    - In test/prod (ENTRA_ID_ENABLED=True): provisioned automatically on
      first sign-in via EntraBackend, matched on entra_oid/entra_tid.
    """

    USERNAME_FIELD = "email"
    email = models.EmailField("email address", unique=True)
    REQUIRED_FIELDS = ["username"]  # only used by `createsuperuser` on the CLI

    # Entra's stable identifiers for the user. e.g. USER Name could change, so adds
    # some redundancy
    # More fields can be added in the future if required (e.g. Department)
    entra_oid = models.UUIDField(null=True, blank=True)
    entra_tid = models.UUIDField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_entra_identity",
                fields=["entra_oid", "entra_tid"],
            )
        ]

    def __str__(self):
        return self.email or self.username
