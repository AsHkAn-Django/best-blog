from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django.conf import settings


class Tag(models.Model):
  title = models.CharField(max_length=264, unique=True)
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('post_new')


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)

    def __str__(self):
        return self.comment


    def get_absolute_url(self):
        return reverse('post')




