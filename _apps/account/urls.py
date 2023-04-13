from django.urls import path
from _apps.account import views

urlpatterns = [
    path("register/", views.register, name="accounts_register"),
]
