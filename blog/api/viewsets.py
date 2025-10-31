from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from . import serializers
from blog.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """List comments for a specific post."""
        post = self.get_object()
        comments = Comment.objects.filter(
            post=post, parent=None).select_related("author")
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
        post_id = self.request.data.get('post')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, parent=parent, post=post)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        """Upvote or downvote a comment."""
        comment = self.get_object()
        action_type = request.data.get('action')

        if action_type == "up":
            comment.upvotes += 1
        elif action_type == "down":
            comment.downvotes += 1
        else:
            return Response(
                {
                'detail': 'Invalid action'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        comment.save()
        return Response({
            'score': comment.score,
            'upvotes': comment.upvotes,
            'downvotes': comment.downvotes
        }, status=status.HTTP_200_OK)