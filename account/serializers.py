from rest_framework import serializers
from account.models import UserProfile, Interest
from django.contrib.auth.models import User
from common.serializers import ImageUploadSerializer
from common.models import ImageUpload
class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['username'] = instance.user.username
        representation['email'] = instance.user.email
        representation['role'] = instance.role.name if instance.role else None
        representation['organization'] = instance.organization.name if instance.organization else None
        representation['interests'] = [interest.name for interest in instance.interests.all()] if instance.interests else None
        profile_pic = ImageUpload.objects.get(id=instance.profile_picture)
        profile_pic = ImageUploadSerializer(instance=profile_pic).data['images']
        if profile_pic:
            representation['profile_picture'] = profile_pic[0]
        else:
            representation['profile_picture'] = "/media/uploads/no_profile_Pic.jpeg"
        return representation


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
