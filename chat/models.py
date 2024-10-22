from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Session(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def end_session(self):
        """Mark the session as ended"""
        self.is_active = False
        self.end_time = timezone.now()
        self.save()

    def __str__(self):
        return self.channel_name


class Recording(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    resource_id = models.CharField(max_length=100)
    sid = models.CharField(max_length=100)
    file_url = models.URLField(max_length=500, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Recording for {self.session.channel_name}"
