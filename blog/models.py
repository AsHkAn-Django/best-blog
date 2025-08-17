from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey



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
    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = models.ManyToManyField(Tag, related_name='posts')
    views = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pub_local = timezone.localtime(self.publish)
        return reverse('post_detail',
                       args=[pub_local.year,
                             pub_local.month,
                             pub_local.day,
                             self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    like = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        ordering = ['-like']
        indexes = [models.Index(fields=['like']),]

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('post')

    def is_reply(self):
        return self.parent is not None


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def get_markdown_path(self):
        if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return f"![alt text]({self.file.url})"
        elif self.file.name.lower().endswith(('.mp4', '.webm')):
            return f"<video controls><source src='{self.file.url}'></video>"
        else:
            return f"[Download file]({self.file.url})"


class Notification(models.Model):
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
