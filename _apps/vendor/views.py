from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from _apps.account.forms import UserProfileForm
from _apps.account.models import UserProfile
from _apps.account.views import logapp, check_role_vendor


from _apps.vendor.forms import VendorRegistrationForm
from _apps.vendor.models import Vendor


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorRegistrationForm(
            request.POST, request.FILES, instance=vendor
        )
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Setting updated")
            return redirect("vendor_profile")
        else:
            logapp.error(profile_form.errors)
            logapp.error(vendor_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorRegistrationForm(instance=vendor)

    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }
    return render(request, "vendor/vendor-profile.html", context)
