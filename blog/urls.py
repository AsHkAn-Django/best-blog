from django.urls import path
from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('post/tag_filter/<int:pk>/', views.TagFilterListView.as_view(), name='tag_filter'),  
    path('post/add_comments/<int:pk>/', views.add_comment, name='add_comment'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),        
    path('search_post/', views.post_search, name='search_post'),
    path('tag/new', views.TagNewView.as_view(), name='tag_new'),
    path('post/new', views.add_new_post, name='post_new'),
    path('post/', views.PostView.as_view(), name='post'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
