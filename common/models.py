import uuid
from django.db import models


class ImageUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return str(self.id)
