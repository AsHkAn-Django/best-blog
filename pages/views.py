from django.views.generic import TemplateView
from .models import FeedBack
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib import messages
from textblob import TextBlob


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'



class AddFeedBackView(LoginRequiredMixin, CreateView):
    model = FeedBack
    fields = ('name', 'email', 'body',)
    template_name = 'add_feedback.html'

    def form_valid(self, form):
        text = form.cleaned_data['body'].strip()
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            message = 'Thank you for your kind words! We’re happy to hear you had a good experience.'
        else:
            message = 'We’re sorry to hear you’re not satisfied. We’ll review your feedback as soon as possible. Thank you for sharing your thoughts with us.'
        messages.success(self.request, message)
        return super().form_valid(form)
