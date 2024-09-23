from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import UserProfileAPI, SignupViewSet


app_name = "account"


router = DefaultRouter()
router.register("user-profile", UserProfileAPI, basename="user-profile")
router.register(r'signup', SignupViewSet, basename='signup')
urlpatterns = [] + router.urls
