from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from charity.models import Category, Donation, Institution, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    permissions_ = (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        },
    )
    personal_info = (_("Personal info"), {"fields": ("first_name", "last_name")})
    account_info = (None, {"fields": ("email", "password")})
    dates = (_("Important dates"), {"fields": ("last_login", "date_joined")})
    fieldsets = (
        account_info,
        personal_info,
        permissions_,
        dates,
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
