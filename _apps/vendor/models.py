from django.db import models

from _apps.account.models import User, UserProfile
from _apps.account.utils import send_notification


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

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                mail_template = "account/emails/admin-approval-email.html"
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved,
                }
                if self.is_approved:
                    # send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send notification email
                    mail_subject = "We're sorry! You're not eligible for publishing your food menu on our marketplace"
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)
