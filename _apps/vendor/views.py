from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

from _apps.account.forms import UserProfileForm
from _apps.account.models import UserProfile
from _apps.account.views import logapp, check_role_vendor
from _apps.account.context_processors import get_vendor_instance

from _apps.menu.forms import CategoryForm, FoodItemForm
from _apps.menu.models import Category, FoodItem

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


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor_instance(request)
    categories = Category.objects.filter(vendor=vendor).order_by("-created_at")

    context = {"categories": categories, "vendor": vendor}
    return render(request, "vendor/menu-builder.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor_instance(request)
    category = get_object_or_404(Category, pk=pk)

    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {"fooditems": fooditems, "category": category}
    return render(request, "vendor/fooditems-by-category.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            category.vendor = get_vendor_instance(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category has been added successfully")
            return redirect("vendor__menu_builder")
        else:
            logapp.error(form.errors)
            error = form.errors
            a = list(error.as_data()["category_name"][0])
            error_message = a[0]
            messages.error(request, error_message)
            return redirect("vendor__menu_builder")
    else:
        form = CategoryForm()

    context = {"form": form}
    return render(request, "vendor/add-category.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            category.vendor = get_vendor_instance(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category updated successfully")
            return redirect("vendor__menu_builder")
        else:
            logapp.error(form.errors)
            error = form.errors
            a = list(error.as_data()["category_name"][0])
            error_message = a[0]
            messages.error(request, error_message)
            return redirect("vendor__menu_builder")
    else:
        form = CategoryForm(instance=category)

    context = {"form": form, "category": category}
    return render(request, "vendor/edit-category.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully")
    return redirect("vendor__menu_builder")


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def add_fooditems(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)

        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor_instance(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item has been added successfully")
            return redirect("vendor__fooditems_by_category", food.category.id)
        else:
            logapp.error(form.errors)
            error = form.errors
            a = list(error.as_data())
            # print(a)
            error_message = a[0]
            messages.error(request, error_message)
            return redirect("vendor__menu_builder")
    else:
        form = FoodItemForm()
        form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor_instance(request)
        )

    context = {"form": form}
    return render(request, "vendor/add-food.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def edit_fooditems(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)

    if request.method == "POST":
        form = FoodItemForm(request.POST, instance=food)

        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor_instance(request)
            food.slug = slugify(food_title)
            food.save()
            messages.success(request, "FoodItem updated successfully")
            return redirect("vendor__fooditems_by_category", food.category.id)
        else:
            logapp.error(form.errors)
            error = form.errors
            a = list(error.as_data())
            # print(a)
            error_message = a[0]
            messages.error(request, error_message)
            return redirect("vendor__menu_builder")
    else:
        form = FoodItemForm(instance=food)
        form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor_instance(request)
        )

    context = {"form": form, "food": food}
    return render(request, "vendor/edit-food.html", context)


@login_required(login_url="accounts_login")
@user_passes_test(check_role_vendor)
def delete_fooditems(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, "Food Item deleted successfully")
    return redirect("vendor__menu_builder")
