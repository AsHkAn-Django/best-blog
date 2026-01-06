from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache

from blog.models import Post
from .models import Comment, Notification


@receiver(post_save, sender=Comment)
def send_reply_notification(sender, instance, created, **kwargs):
    # Only for new comments that are replies (have a parent)
    if created and instance.parent and instance.parent.author:
        recipient = instance.parent.author
        message = f"{instance.author.username} replied to your comment."

        # Save in DB
        notification = Notification.objects.create(recipient=recipient, message=message)

        # Send via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",  # group name per user
            {
                "type": "send_notification",
                "content": {"id": notification.id, "message": message},
            },
        )
        print(f"Sending notification to user {recipient.id}: {message}")


POST_CACHE_VERSION_KEY = "post_cache_version"


def get_post_cache_verion():
    """Get current cache version for Post-related caches."""
    version = cache.get(POST_CACHE_VERSION_KEY)
    if version is None:
        version = 1
        cache.set(POST_CACHE_VERSION_KEY, version)
    return version


def bump_post_cache_version():
    """Increment version to invalidate Post-related caches."""
    version = get_post_cache_verion() + 1
    cache.set(POST_CACHE_VERSION_KEY, version)
    return version


@receiver([post_save, post_delete], sender=Post)
def clear_post_cache(sender, **kwargs):
    """Whenever a Post is saved/deleted, bump version => invalidate caches."""
    bump_post_cache_version()
