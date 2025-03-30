from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django.conf import settings
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



class Tag(models.Model):
  title = models.CharField(max_length=264, unique=True)
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('post_new')


class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    
    title = models.CharField(max_length=250)
    # So now we won't have more than one slug with the same publish date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = models.ManyToManyField(Tag, related_name='posts')
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', 
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('post')




