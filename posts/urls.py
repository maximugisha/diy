from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import PostAPI, PostLikeView

app_name = "posts"


router = DefaultRouter()
router.register("posts", PostAPI, basename="posts")
urlpatterns = [path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
               ] + router.urls
