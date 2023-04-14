"""
Project's URLs
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", views.home, name="home"),
    path("accounts/", include("_apps.account.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
