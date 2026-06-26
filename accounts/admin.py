from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ("email",)

    list_display = (
        "email",
        "username",
        "role",
        "email_verified",
        "is_active",
    )

    list_filter = (
        "role",
        "email_verified",
        "is_active",
    )

    search_fields = (
        "email",
        "username",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone_number",
                    "role",
                    "profile_picture",
                    "email_verified",
                )
            },
        ),
    )