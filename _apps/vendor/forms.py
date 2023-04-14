from django import forms

from _apps.vendor.models import Vendor


class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            "vendor_name",
            "vendor_license",
        )
