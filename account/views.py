from rest_framework import viewsets
from rest_framework.response import Response
from account.models import UserProfile, Role, Organization, Interest
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework import permissions
from account.serializers import RoleSerializer, InterestSerializer, OrganizationSerializer


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


class RoleAPI(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class OrganizationAPI(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class InterestAPI(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
