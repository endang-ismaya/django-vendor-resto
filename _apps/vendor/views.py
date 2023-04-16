from django.shortcuts import render, get_object_or_404
from _apps.account.forms import UserProfileForm
from _apps.account.models import UserProfile

from _apps.vendor.forms import VendorRegistrationForm
from _apps.vendor.models import Vendor


def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorRegistrationForm(instance=vendor)

    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }
    return render(request, "vendor/vendor-profile.html", context)
