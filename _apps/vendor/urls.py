from django.urls import path
from _apps.vendor import views

urlpatterns = [
    path("profile/", views.vendor_profile, name="vendor_profile"),
]
