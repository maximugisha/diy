from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import UserProfileAPI, SignupViewSet, RoleAPI, OrganizationAPI, InterestAPI


app_name = "account"


router = DefaultRouter()
router.register("user-profile", UserProfileAPI, basename="user-profile")
router.register(r'signup', SignupViewSet, basename='signup')
router.register("roles", RoleAPI, basename="roles")
router.register("organizations", OrganizationAPI, basename="organizations")
router.register("interests", InterestAPI, basename="interests")
urlpatterns = [] + router.urls
