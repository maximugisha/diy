from django.db import models
import uuid
from django.contrib.auth.models import User
from common.models import ImageUpload, created_since


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    images = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)

    def __str__(self):
        return self.content[:20]

    @property
    def created_since_property(self):
        return created_since(self)
