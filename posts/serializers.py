from rest_framework import serializers
from .models import Post
from common.models import ImageUpload
from common.serializers import MinimalUploadSerializer
from account.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(
        allow_empty=False, child=serializers.UUIDField()
    )

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['user', 'likes', 'created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)

        # Attach images to the post
        for image_uuid in images_data:
            try:
                image = ImageUpload.objects.get(id=image_uuid)
                post.images.add(image)
            except ImageUpload.DoesNotExist:
                raise serializers.ValidationError(f"Image with UUID {image_uuid} does not exist.")

        post.save()
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        img = MinimalUploadSerializer(
            instance=instance.images, many=True
        )
        representation["images"] = [image["image"] for image in img.data]
        representation["likes"] = instance.likes.count()
        representation["user"] = UserProfileSerializer(instance.user.user_profile).data
        return representation
