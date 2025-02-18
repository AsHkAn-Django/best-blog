from django.urls import path
from .views import HomeView, AddFeedBackView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_feedback/', AddFeedBackView.as_view(), name='add_feedback'),
]
