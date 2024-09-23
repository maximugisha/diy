from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='user_profile')
    profile_picture = models.UUIDField(editable=True, default=uuid.uuid4)
    biography = models.TextField(max_length=500, blank=True, null=True)
    interests = models.ManyToManyField('account.Interest', related_name='interests', blank=True, null=True)
    role = models.ForeignKey(Role, related_name='user_role', blank=True, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='user_organization',
                                     blank=True, null=True, on_delete=models.CASCADE
                                     )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def bio(self):
        if self.biography:
            return self.biography[:150]
        else:
            return ""
