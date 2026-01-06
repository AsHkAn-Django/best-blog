from django.views.generic import TemplateView
from .models import FeedBack
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib import messages
from textblob import TextBlob
from blog.tasks import send_feedback_mail


class HomeView(TemplateView):
    template_name = "home.html"


class AddFeedBackView(LoginRequiredMixin, CreateView):
    model = FeedBack
    fields = (
        "name",
        "email",
        "body",
    )
    template_name = "add_feedback.html"

    def form_valid(self, form):
        text = form.cleaned_data["body"].strip()
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        print(sentiment_score)
        if sentiment_score > 0.1:
            form.instance.sentiment = FeedBack.Sentiment.POSITIVE
            message = """Thank you for your kind words!
            We’re happy to hear you had a good experience."""
        elif sentiment_score < -0.1:
            form.instance.sentiment = FeedBack.Sentiment.NEGATIVE
            message = """We’re sorry to hear you’re not satisfied.
            We’ll review your feedback as soon as possible.
            Thank you for sharing your thoughts with us."""
        else:
            form.instance.sentiment = FeedBack.Sentiment.NEUTRAL
            message = """Thanks for your feedback. We try our best
            to get better everyday and improve your experience.:)"""

        send_feedback_mail.delay(
            form.cleaned_data["email"], form.cleaned_data["name"], message
        )
        messages.success(self.request, message)
        return super().form_valid(form)
