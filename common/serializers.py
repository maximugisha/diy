from rest_framework import serializers
from .models import ImageUpload


class MinimalUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['image']


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'image']

    def create(self, validated_data):
        image_upload = ImageUpload.objects.create(**validated_data)
        return image_upload
