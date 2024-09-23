from django.db import models

from django.contrib.auth.models import User
from common.models import ImageUpload


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    images = models.ManyToManyField(ImageUpload, related_name='posts', blank=True)  # Many-to-many relationship

    def __str__(self):
        return self.content[:20]
