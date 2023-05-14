from django.urls import path
from _apps.vendor import views
from _apps.account import views as account_views

urlpatterns = [
    path("", account_views.vendor_dashboard, name="vendor_dashboard"),
    path("profile/", views.vendor_profile, name="vendor_profile"),
    path("menu-builder/", views.menu_builder, name="vendor__menu_builder"),
    path(
        "menu-builder/category/<int:pk>",
        views.fooditems_by_category,
        name="vendor__fooditems_by_category",
    ),
    # category crud
    path("menu-builder/category/add/", views.add_category, name="vendor__add_category"),
    path(
        "menu-builder/category/edit/<int:pk>/",
        views.edit_category,
        name="vendor__edit_category",
    ),
    path(
        "menu-builder/category/delete/<int:pk>/",
        views.delete_category,
        name="vendor__delete_category",
    ),
    # fooditems crud
    path(
        "menu-builder/fooditems/add/",
        views.add_fooditems,
        name="vendor__add_fooditems",
    ),
    path(
        "menu-builder/fooditems/edit/<int:pk>/",
        views.edit_fooditems,
        name="vendor__edit_fooditems",
    ),
    path(
        "menu-builder/fooditems/delete/<int:pk>/",
        views.delete_fooditems,
        name="vendor__delete_fooditems",
    ),
]
