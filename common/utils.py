import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = getattr(settings, 'ALLOWED_EXTENSIONS',
                               ['.mp4', '.zip', '.jpeg', '.jpg', '.png', '.py', '.ino', '.txt', '.pdf', '.doc', '.docx',
                                '.ppt', '.pptx'])
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))


def validate_file_size(value):
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)  # 2 MB
    if value.size > max_size:
        raise ValidationError(_('File size exceeds the maximum allowed size.'))


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename, [1] returns file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png, .gif.'))
