from rest_framework import serializers
from blog.models import Post, Tag, Comment



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'author', 'created', 'updated', 'active']
        read_only_fields = ['id', 'author', 'active']
        
    def get_author(self, obj):
        return obj.author.username


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'title']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'publish', 'created', 'updated', 'body', 'status', 'tags', 'comments']

    def get_author(self, obj):
        return obj.author.username