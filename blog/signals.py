from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Comment, Notification

@receiver(post_save, sender=Comment)
def send_reply_notification(sender, instance, created, **kwargs):
    # Only for new comments that are replies (have a parent)
    if created and instance.parent and instance.parent.author:
        recipient = instance.parent.author
        message = f"{instance.author.username} replied to your comment."

        # Save in DB
        Notification.objects.create(recipient=recipient, message=message)

        # Send via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",  # group name per user
            {
                "type": "send_notification",
                "content": {
                    "message": message
                }
            }
        )
        print(f"Sending notification to user {recipient.id}: {message}")

