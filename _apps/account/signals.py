import logging


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from _apps.account.models import User, UserProfile

logapp = logging.getLogger("app")


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        logapp.info(
            f"post_save receiver: creating the user profile for {instance.email}"
        )
        UserProfile.objects.create(user=instance)

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            logapp.info(f"post_save receiver: {instance.email} has updated his profile")
        except UserProfile.DoesNotExist:
            logapp.info(
                f"post_save receiver: Profile was not exists, create the user profile for {instance.email}"
            )
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    logapp.info(f"pre_save receiver: {instance.username}")

    if not instance.email:
        instance.email = instance.username
        logapp.info(
            f"pre_save receiver: {instance.username}'s email was not provided during creation"
        )

    if not instance.username:
        instance.username = instance.email
        logapp.info(
            f"pre_save receiver: {instance.email}'s username was not provided during creation"
        )
