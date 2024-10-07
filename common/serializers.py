from rest_framework import serializers
from .models import ImageUpload, UploadedImage


class ImageUploadSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.FileField(), write_only=True)
    images_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageUpload
        fields = ['id', 'images', 'images_url']

    def create(self, validated_data):
        images = validated_data.pop('images')
        image_upload = ImageUpload.objects.create(**validated_data)

        for image in images:
            UploadedImage.objects.create(image_upload=image_upload, image=image)

        return image_upload

    def get_images_url(self, obj):
        return [image.image.url for image in obj.images.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = self.get_images_url(instance)
        return representation
