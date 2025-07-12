from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from . import serializers
from blog.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == 'POST':
            serializer = serializers.CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = serializers.CommentSerializer(comments, many=True)
            return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'comments':
            return serializers.CommentSerializer
        return super().get_serializer_class()