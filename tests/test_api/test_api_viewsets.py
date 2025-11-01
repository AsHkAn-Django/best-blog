import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from blog.models import Post, Tag, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPostViewSet:
    def setup_method(self, method):
        self.client = APIClient()
        self.user = User.objects.create_user(username="ashkan", password="pass123")
        self.client.force_authenticate(user=self.user)

        self.tag = Tag.objects.create(title="django")
        self.post = Post.objects.create(
            title="Test Post",
            body="Body of test post",
            author=self.user,
            status=Post.Status.PUBLISHED
        )
        self.post.tags.add(self.tag)

    def test_list_posts(self):
        url = reverse("posts-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1
        assert response.data[0]['title'] == "Test Post"

    def test_create_post(self):
        url = reverse("posts-list")
        tag = Tag.objects.create(title="python")
        data = {
            "title": "New Post",
            "body": "New post body",
            "status": "PB",      # include status to be explicit
            "tag_ids": [tag.id],
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code in [200, 201]
        assert response.data['title'] == "New Post"


@pytest.mark.django_db
class TestCommentViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="ashkan",
            password="pass123"
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Post for comments",
            body="post body",
            author=self.user,
            status=Post.Status.PUBLISHED,
        )

    def test_create_comment(self):
        url = reverse("comments-list")
        data = {"post": self.post.id, "comment": "This is a comment"}
        response = self.client.post(url, data, format="json")
        assert response.status_code in [200, 201]
        assert Comment.objects.filter(comment="This is a comment").exists()

    def test_vote_up_comment(self):
        comment = Comment.objects.create(
            post=self.post, comment="Vote me", author=self.user
        )
        url = reverse("comments-vote", args=[comment.id])
        response = self.client.post(url, {"action": "up"}, format="json")
        comment.refresh_from_db()
        assert response.status_code == 200
        assert comment.upvotes == 1
        assert response.data['score'] == 1

    def test_vote_down_comment(self):
        comment = Comment.objects.create(
            post=self.post, comment="Vote me down", author=self.user
        )
        url = reverse("comments-vote", args=[comment.id])
        response =self.client.post(url, {"action": "down"}, format="json")
        comment.refresh_from_db()
        assert response.status_code == 200
        assert comment.downvotes == 1
        assert response.data['score'] == -1

    def test_invalid_vote_action(self):
        comment = Comment.objects.create(
            post=self.post, comment="Invalid vote", author=self.user
        )
        url = reverse("comments-vote", args=[comment.id])
        response = self.client.post(url, {"action": "invalid"}, format="json")
        assert response.status_code == 400
        assert "Invalid action" in response.data['detail']

