from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import Post, Comment, Tag, Media, Notification
from pages.models import FeedBack


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)  # Registers the Post model with the Django admin panel
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]

    prepopulated_fields = {'slug': ('title',)}

    list_display = ['title', 'slug', 'author', 'publish', 'status']
    # Defines which fields are shown in the admin post list view

    list_filter = ['status', 'created', 'publish', 'author']
    # Adds filters in the admin sidebar to filter posts by these fields

    search_fields = ['title', 'body']
    # Enables a search box in the admin to search posts by title or body content

    raw_id_fields = ['author']
    # Displays an author lookup field instead of a dropdown for better performance on large datasets

    date_hierarchy = 'publish'
    # Adds a date-based navigation bar in the admin panel for filtering by the publish date

    ordering = ['status', 'publish']
    # Sets default ordering of posts: first by status, then by publish date

    show_facets = admin.ShowFacets.ALWAYS
    # Show the number of ovjwcts corresponding to each specific filter

@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('comment','created', 'parent')
    mptt_level_indent = 20  # pixels to indent per level


@admin.register(FeedBack)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'body', 'created_at', 'colored_sentiment']

    def colored_sentiment(self, obj):
        display = obj.get_sentiment_display()
        color = {
            'Positive': 'green',
            'Negative': 'red',
            'Neutral': 'orange'
        }.get(display, 'black')

        return format_html('<span style="color: {};">{}</span>', color, display)

    colored_sentiment.short_description = 'Sentiment'


admin.site.register(Notification)
admin.site.register(Tag)
admin.site.register(Media)
admin.site.register(IntervalSchedule)
admin.site.register(PeriodicTask)
