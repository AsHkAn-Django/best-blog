from django.urls import path
from .views import (PostDetailView, PostUpdateView,
                    PostDeleteView, PostNewView, PostView, TagNewView, TagFilterListView, add_comment)

urlpatterns = [
    path('post/tag_filter/<int:pk>/', TagFilterListView.as_view(), name='tag_filter'),  
    path('post/add_comments/<int:pk>/', add_comment, name='add_comment'),
    path('tag/new', TagNewView.as_view(), name='tag_new'),
    path('post/new', PostNewView.as_view(), name='post_new'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/', PostView.as_view(), name='post'),
]
