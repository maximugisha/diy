from rest_framework import viewsets
from .models import Session, Recording
from .serializers import SessionSerializer, RecordingSerializer


class SessionAPI(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class RecordingAPI(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
