from django.urls import path
from _apps.account import views

urlpatterns = [
    path("register/", views.register, name="accounts_register"),
    path("register-vendor/", views.register_vendor, name="accounts_register_vendor"),
    path("login/", views.login, name="accounts_login"),
    path("logout/", views.logout, name="accounts_logout"),
    path("dashboard/", views.dashboard, name="accounts_dashboard"),
]
