from . import viewsets
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', viewsets.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]