from django.contrib import admin

from common.models import ImageUpload, UploadedImage


# Register your models here.
@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(UploadedImage)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
