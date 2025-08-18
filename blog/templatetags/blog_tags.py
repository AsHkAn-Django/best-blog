from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.core.cache import cache
import markdown

from blog.models import Post
from blog.signals import get_post_cache_verion



register = template.Library()


@register.simple_tag
def total_posts():
    version = get_post_cache_verion()
    total_posts = cache.get('total_posts', version=version)
    if total_posts is None:
        total_posts = Post.published.count()
        cache.set('total_posts', total_posts, 300, version=version)
    return total_posts


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    version = get_post_cache_verion()
    key = f'latest_posts_{count}'
    latest_posts = cache.get(key, version=version)
    if latest_posts is None:
        latest_posts = Post.published.order_by('-publish')[:count]
        cache.set(key, latest_posts, 300, version=version)
    return{'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    version = get_post_cache_verion()
    key = f'most_commented_{count}'
    most_commented = cache.get(key, version=version)
    if most_commented is None:
        most_commented = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
        cache.set(key, most_commented, 300, version=version)
    return most_commented


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