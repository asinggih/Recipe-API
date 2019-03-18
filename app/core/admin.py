from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# This is just to make sure that the string is in
# user readable format. e.g, when we hv different language
# support it can be translated properly
from django.utils.translation import gettext as _

from . import models


class UserAdmin(BaseUserAdmin):
    # Items requried when EDITING a user
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password",
            ),
        }),
        (_('Personal Info'), {
            "fields": (
                "name",
            )
        }),
        (_('Permissions'), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
        (_('Important dates'), {
            "fields": (
                "last_login",
            )
        })
    )

    # Fieldsets required when ADDING a new user
    add_fieldsets = (
        (None, {
            "classes": (
                "wide",
            ),
            "fields": (
                "email", "password1", "password2"
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
