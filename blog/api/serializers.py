from rest_framework import serializers
from blog.models import Post, Tag, Comment
from django.utils.text import slugify


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'comment', 'author', 'created', 'parent',
            'updated', 'active', 'children', 'upvotes', 'downvotes'
        ]
        read_only_fields = ['id', 'author', 'active']

    def get_author(self, obj):
        return obj.author.username


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False
    )
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author',
            'publish', 'created', 'updated',
            'body', 'status', 'tags', 'tag_ids', 'comments'
        ]
        read_only_fields = ('slug', 'author', 'publish', 'created', 'updated')

    def create(self, validated_data):
        tags = validated_data.pop("tag_ids", [])
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def get_author(self, obj):
        return obj.author.username

    def get_comments(self, obj):
        top_comments = obj.comments.filter(parent=None)
        return CommentSerializer(top_comments, many=True).data
