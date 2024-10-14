from rest_framework.routers import DefaultRouter
from django.urls import path

from .api import SessionAPI, RecordingAPI
from .views import start_session

app_name = "chat"

router = DefaultRouter()
router.register("sessions", SessionAPI, basename="sessions")
router.register("recordings", RecordingAPI, basename="recordings")
urlpatterns = [
                  path('start-session/', start_session, name='start-session'),
              ] + router.urls
