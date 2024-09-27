import os
from django.db import models
import uuid
from django.contrib.auth.models import User
from common.models import ImageUpload, created_since
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from djrichtextfield.models import RichTextField


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = getattr(settings, 'ALLOWED_EXTENSIONS',
                               ['.mp4', '.zip', '.jpeg', '.jpg', '.png', '.py', '.ino', '.txt'])
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))


def validate_file_size(value):
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 2 * 1024 * 1024)  # 2 MB
    if value.size > max_size:
        raise ValidationError(_('File size exceeds the maximum allowed size.'))


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["id"]  # Set your default ordering here


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


class Resource(BaseModel):
    class Audience(models.TextChoices):
        public = 'public', _('Public')
        organization = 'organization', _('My Organization')
        draft = 'draft', _('Draft')

    class Type(models.TextChoices):
        video = 'video', _('Video')
        image = 'image', _('Image')
        pdf = 'pdf', _('PDF')
        document = 'document', _('Document')
        zip = 'zip', _('Zip')

    title = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, max_length=20, default=Type.pdf)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    attachment = models.FileField(upload_to="attachments", validators=[
        validate_file_extension, validate_file_size])
    attachment_name = models.CharField(max_length=255)
    attachment_size = models.IntegerField()  # Store file size in bytes
    attachment_extension = models.CharField(max_length=20)
    audience = models.CharField(choices=Audience.choices, max_length=20, default=Audience.public)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.pk:  # Only perform these operations when creating a new instance
            self.attachment_name = self.attachment.name
            self.attachment_size = self.attachment.size
            self.attachment_extension = get_file_extension(self.attachment_name)

        super(Resource, self).save(*args, **kwargs)
