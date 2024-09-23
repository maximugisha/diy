from rest_framework.routers import DefaultRouter

from .views import UploadAPI

app_name = "common"


router = DefaultRouter()
router.register("upload", UploadAPI, basename="upload-service")
urlpatterns = [] + router.urls
