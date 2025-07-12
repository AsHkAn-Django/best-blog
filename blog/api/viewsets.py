from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from . import serializers
from blog.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = serializers.PostSerializer

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            data = request.data
            serializer = serializers.CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            post = get_object_or_404(Post, pk=pk)
            comments = Comment.objects.filter(post=post)
            serializer = serializers.CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data}, status.HTTP_200_OK)
