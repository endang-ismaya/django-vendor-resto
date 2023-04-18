from django import forms

from _apps.vendor.models import Vendor
from _apps.account.validators import allow_only_images_validator


class VendorRegistrationForm(forms.ModelForm):
    vendor_license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images_validator],
    )

    class Meta:
        model = Vendor
        fields = (
            "vendor_name",
            "vendor_license",
        )
