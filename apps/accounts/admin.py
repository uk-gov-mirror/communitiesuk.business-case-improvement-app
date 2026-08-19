from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    ordering = ("email",)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Entra ID", {"fields": ("entra_oid", "entra_tid")}),
    )
    readonly_fields = ("entra_oid", "entra_tid")
