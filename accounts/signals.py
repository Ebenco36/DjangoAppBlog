from django.conf import settings
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile


# user model
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates user profile on successful registration
    :param instance: user object instance
    :param created: boolean to check if account was created rather than saved
    :param kwargs: other args
    :return:
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Updates user profile on successful registration
    :param instance: user object instance
    :param created: boolean to check if account was created rather than saved
    :param kwargs: other args
    :return:
    """
    instance.profile.save()


