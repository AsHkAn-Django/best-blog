import graphene
from graphene_django.types import DjangoObjectType
from blog.models import Post, Comment, Tag
from django.contrib.auth import get_user_model


# STEP1:  Type Definitions
class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "title")


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "comment", "author", "created", "active")


class PostType(DjangoObjectType):
    author = graphene.Field(UserType)
    comments = graphene.List(CommentType)
    tags = graphene.List(TagType)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "publish",
            "body",
            "tags",
            "comments",
        )

    def resolve_comments(self, info):
        return self.comments.filter(active=True)

    def resolve_tags(self, info):
        return self.tags.all()


# STEP2: Queries
class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    def resolve_all_posts(root, info):
        return Post.published.all()

    def resolve_post(root, info, id):
        return Post.published.get(pk=id)


# STEP3: Mutations
class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        comment = graphene.String(required=True)

    comment_obj = graphene.Field(CommentType)

    def mutate(self, info, post_id, comment):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        post = Post.objects.get(pk=post_id)
        comment_obj = Comment.objects.create(
            post=post, author=user, comment=comment, active=False
        )
        return CreateComment(comment_obj=comment_obj)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()


# STEP4: Root Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
