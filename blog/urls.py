from django.urls import path
from .views import (PostDetailView, PostUpdateView,
                    PostDeleteView, PostNewView, PostView)

urlpatterns = [
    path('post/new', PostNewView.as_view(), name='post_new'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostView.as_view(), name='post'),
]
