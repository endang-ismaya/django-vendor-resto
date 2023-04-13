from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from _apps.account.forms import UserRegistrationForm
from _apps.account.models import User


# Create your views here.
def register(request):
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

            messages.success(request, "Your account has been registered successfully!")
            return redirect(reverse("home"))
        else:
            context = {"form": form}
            return render(request, "account/register.html", context)
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "account/register.html", context)
