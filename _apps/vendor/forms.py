from django import forms

from _apps.vendor.models import Vendor


class VendorRegistrationForm(forms.ModelForm):
    vendor_license = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"})
    )

    class Meta:
        model = Vendor
        fields = (
            "vendor_name",
            "vendor_license",
        )
