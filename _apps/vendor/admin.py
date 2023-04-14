from django.contrib import admin

from _apps.vendor.models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "vendor_name",
        "is_approved",
        "created_at",
        "modified_at",
    )
    link_display_links = (
        "user",
        "vendor_name",
    )


admin.site.register(Vendor, VendorAdmin)
