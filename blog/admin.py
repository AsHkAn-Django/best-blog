from django.contrib import admin

from .models import Post, Comment


# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
