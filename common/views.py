from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .models import ImageUpload
from .serializers import ImageUploadSerializer


class UploadAPI(ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]
