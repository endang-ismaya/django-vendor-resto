from django.urls import path, include
from _apps.account import views

urlpatterns = [
    path("", views.my_account),
    path("register/", views.register, name="accounts_register"),
    path("register-vendor/", views.register_vendor, name="accounts_register_vendor"),
    path("login/", views.login, name="accounts_login"),
    path("logout/", views.logout, name="accounts_logout"),
    path(
        "customer-dashboard/",
        views.customer_dashboard,
        name="accounts_customer_dashboard",
    ),
    path(
        "vendor-dashboard/",
        views.vendor_dashboard,
        name="accounts_vendor_dashboard",
    ),
    path("my-account/", views.my_account, name="accounts_myaccount"),
    path("activate/<uidb64>/<token>/", views.activate, name="accounts_activate"),
    path("forgot-password/", views.forgot_password, name="accounts_forgot_password"),
    path(
        "reset-password-validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="accounts_reset_password_validate",
    ),
    path("reset-password/", views.reset_password, name="accounts_reset_password"),
    path("vendor/", include("_apps.vendor.urls")),
]
