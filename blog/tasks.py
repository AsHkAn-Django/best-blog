from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_feedback_mail(email_address, username, message):
    """
    Send a feedback confirmation email to the user.
    """
    subject = "Feedback Confirmation"
    message_body = f"Hi dear {username}!\n\n{message}"
    send_mail(
        subject=subject,
        message=message_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_address],
        fail_silently=False
    )