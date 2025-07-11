from rest_framework import viewsets
from . import serializers
from blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = serializers.PostSerializer
    