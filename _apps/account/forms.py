from django import forms
from _apps.account.models import User, UserProfile
from _apps.account.validators import allow_only_images_validator


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        )

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password", None)
        confirm_password = cleaned_data.get("confirm_password", None)

        if len(password) < 8:
            raise forms.ValidationError("Password should be min 8 chars")

        if password != confirm_password:
            raise forms.ValidationError("Password do not match!")


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images_validator],
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images_validator],
    )

    class Meta:
        model = UserProfile
        fields = (
            "profile_picture",
            "cover_photo",
            "address_line_1",
            "address_line_2",
            "country",
            "city",
            "pin_code",
            "latitude",
            "longitude",
        )
