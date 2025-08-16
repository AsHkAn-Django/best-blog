from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from blog.models import Post
from django.core.cache import cache



@shared_task
def send_feedback_mail(email_address, name, message):
    """
    Send a feedback confirmation email to the user.
    """
    subject = "Feedback Confirmation"
    message_body = f"Hi dear {name}!\n\n{message}"
    send_mail(
        subject=subject,
        message=message_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_address],
        fail_silently=False
    )


@shared_task
def update_posts_view_from_cache():
    for post in Post.objects.all():
        cache_key = f'post_{post.id}_views'
        views = cache.get(cache_key)
        if views:
            post.views = views
            post.save(update_fields=['views'])
