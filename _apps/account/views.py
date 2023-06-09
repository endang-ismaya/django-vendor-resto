import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from _apps.account.forms import UserRegistrationForm
from _apps.account.models import User, UserProfile
from _apps.account.utils import (
    detect_user,
    send_password_reset_email,
    send_verification_email,
)
from _apps.vendor.forms import VendorRegistrationForm

logapp = logging.getLogger("app")


# custom decorator restrict the vendor from accessing customer page vice versa
def check_role_vendor(user):
    if user.role == 1:
        return True

    raise PermissionDenied("Not Authorized to access the page!")


def check_role_customer(user):
    if user.role == 2:
        return True

    raise PermissionDenied("Not Authorized to access the page!")


def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You've been registered, no need to register anymore!")
        return redirect(reverse("accounts_myaccount"))

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # new_user = form.save(commit=False)
            # new_user.set_password(form.cleaned_data["password"])
            # new_user.save()

            # other ways using models User
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            # send email verification
            send_verification_email(request, user)
            messages.success(request, "Your account has been registered successfully!")
            return redirect(reverse("home"))
        else:
            context = {"form": form}
            return render(request, "account/register.html", context)
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "account/register.html", context)


def register_vendor(request):
    if request.user.is_authenticated:
        messages.info(request, "You've been registered, no need to register anymore!")
        return redirect(reverse("accounts_myaccount"))

    if request.method == "POST":
        # store the data and create the user
        form = UserRegistrationForm(request.POST)
        vendor_form = VendorRegistrationForm(request.POST, request.FILES)

        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.phone_number = phone_number
            user.role = User.VENDOR
            user.save()

            # vendor
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send email verification
            send_verification_email(request, user)
            messages.success(
                request,
                "Your account has been registered successfully!, please wait for the approval",
            )
            return redirect(reverse("accounts_register_vendor"))
        else:
            logapp.error(form.errors)
    else:
        form = UserRegistrationForm()
        vendor_form = VendorRegistrationForm()

    context = {"form": form, "vendor_form": vendor_form}
    return render(request, "account/register-vendor.html", context)


def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are logged in, no need to login anymore!")
        return redirect(reverse("accounts_myaccount"))

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("accounts_myaccount")
        else:
            messages.error(request, "Error logging In - Please try it again.")
            return redirect("accounts_login")

    return render(request, "account/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts_login")


@login_required(login_url="accounts_login")
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, "account/customer-dashboard.html")


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, "account/vendor-dashboard.html")


@login_required(login_url="accounts_login")
def my_account(request):
    redirect_url = detect_user(request.user)
    return redirect(reverse(redirect_url))


def activate(request, uidb64, token):
    """
    activate the user by setting the is_active status to True
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated.")
        return redirect("accounts_myaccount")
    else:
        messages.error(request, "Invalid user or activation link")
        return redirect("accounts_login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            send_password_reset_email(request, user)
            messages.info(request, "Password reset link has been sent to your mail.")
            return redirect("accounts_login")
        else:
            messages.error(request, "Email not exists or not registered.")
            return redirect("accounts_forgot_password")

    return render(request, "account/forgot-password.html")


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password")
        return redirect("accounts_reset_password")
    else:
        messages.error(request, "Invalid reset link")
        return redirect("accounts_login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset done.")
            return redirect("accounts_login")
        else:
            messages.error(request, "Password mismatch!")
            return redirect("accounts_reset_password")

    return render(request, "account/reset-password.html")
