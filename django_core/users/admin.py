from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "date_joined",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "date_joined",
    )
    list_filter = (
        "role",
    )
    ordering = (
        "email",
        "date_joined",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "middle_name",
    )
