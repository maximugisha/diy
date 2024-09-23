from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from account.models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework import decorators, permissions


# Create your views here.
class UserProfileAPI(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)

        return queryset


class SignupViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data)

