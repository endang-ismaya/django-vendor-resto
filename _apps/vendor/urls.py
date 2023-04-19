from django.urls import path
from _apps.vendor import views
from _apps.account import views as account_views

urlpatterns = [
    path("", account_views.vendor_dashboard, name="vendor_dashboard"),
    path("profile/", views.vendor_profile, name="vendor_profile"),
    path("menu-builder/", views.menu_builder, name="vendor__menu_builder"),
]
