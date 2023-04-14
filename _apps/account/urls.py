from django.urls import path
from _apps.account import views

urlpatterns = [
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
]
