from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


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


class CustomUserProfile(admin.ModelAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = (
        "user_email",
        "user_role",
        "address",
    )
    ordering = ("-created_at",)
    exclude = ("password",)

    def user_role(self, x):
        return x.user.get_role()

    def user_email(self, x):
        return x.user.email


# registration
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, CustomUserProfile)
