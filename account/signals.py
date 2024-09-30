from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import UserProfile
from decouple import config


def get_default_profile_picture():
    return config('DEFAULT_PROFILE_PICTURE')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, profile_picture=get_default_profile_picture)
