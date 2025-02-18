from django.views.generic import TemplateView
from .models import FeedBack
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib import messages


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    

class AddFeedBackView(LoginRequiredMixin, CreateView):
    model = FeedBack
    fields = ('name', 'email', 'body',)
    template_name = 'add_feedback.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Thanks for your feedback. We will review it as soon as possible.')
        return super().form_valid(form)
