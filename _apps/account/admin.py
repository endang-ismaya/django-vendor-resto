from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "username",
        "is_staff",
        "is_active",
        "last_login",
    )
    ordering = ("-date_joined",)


admin.site.register(User, CustomUserAdmin)
