from django.db import models

from _apps.account.models import User, UserProfile


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name="uservendor", on_delete=models.CASCADE
    )
    user_profile = models.OneToOneField(
        UserProfile, related_name="userprofile", on_delete=models.CASCADE
    )
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to="vendors/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
