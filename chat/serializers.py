from rest_framework import serializers
from .models import Session, Recording
from account.serializers import UserSerializer

class SessionSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)

    class Meta:
        model = Session
        fields = '__all__'


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'
