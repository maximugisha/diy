import uuid
from django.db import models
from django.utils import timezone
from common.utils import validate_image_extension

def created_since(model):
    now = timezone.now()  # Use Django's timezone-aware current time
    diff = now - model.created_at
    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} s"
    elif seconds < 3600:
        return f"{int(seconds // 60)} m"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} h"
    else:
        return model.created_at.strftime("%d/%m/%Y")


class ImageUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)


class UploadedImage(models.Model):
    image_upload = models.ForeignKey(ImageUpload, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', validators=[
        validate_image_extension])

    def __str__(self):
        return str(self.image)
