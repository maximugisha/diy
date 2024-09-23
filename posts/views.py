from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response


class PostAPI(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return Response({'likes_count': post.likes.count()})
