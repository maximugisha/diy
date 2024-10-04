from django.db import models
import uuid
from django.contrib.auth.models import User
from common.models import ImageUpload, created_since
from django.utils.translation import gettext_lazy as _
from common.utils import validate_file_extension, validate_file_size, get_file_extension


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
    content = models.TextField()
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
