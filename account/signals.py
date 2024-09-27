from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, profile_picture="56b442f5-86b0-4aa3-8b04-826d62972c9a")
