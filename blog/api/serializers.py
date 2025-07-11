from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'publish', 'created', 'updated', 'body', 'status', 'tags']