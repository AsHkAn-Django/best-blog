from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return{'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['fenced_code', 'codehilite']))


@register.filter
def is_video(file_url):
    return file_url.lower().endswith('.mp4')


@register.inclusion_tag('comment_list.html', takes_context=True)
def render_comments(context, comments, depth=0):
    """
    Renders a list of comments and their children recursively. comments should be a queryset or
    list of comment instances. depth is used to indent nested lists.
    """
    return {'comments': comments, 'depth': depth, 'request': context['request']}