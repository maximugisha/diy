from rest_framework import serializers
from .models import Post, Resource
from common.models import ImageUpload
from common.serializers import ImageUploadSerializer
from account.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    created_since = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "content", "images", "created_since", "likes"]

    def get_created_since(self, obj):
        return obj.created_since_property

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            images = ImageUpload.objects.get(id=instance.images)
            representation["images"] = ImageUploadSerializer(instance=images).data['images']
        except ImageUpload.DoesNotExist:
            representation["images"] = []

        representation["likes"] = instance.likes.count()
        representation["user"] = UserProfileSerializer(instance.user.user_profile).data
        return representation


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"
        read_only_fields = ['created_at', 'user', 'attachment_extension', 'attachment_size', 'attachment_name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserProfileSerializer(instance.user.user_profile).data
        return representation
