from django.db import models
from django.urls import reverse


# Create your models here.
class FeedBack(models.Model):
    '''Feedback from a user that only admin can read it.'''

    class Sentiment(models.TextChoices):
        POSITIVE = 'POSI', 'Positive'
        NEUTRAL = 'NEUT', 'Neutral'
        NEGATIVE = 'NEGA', 'Negative'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=4, choices=Sentiment.choices, default=Sentiment.NEUTRAL)

    def __str__(self):
        return f"{self.name}: {self.body[:100]} ..."

    def get_absolute_url(self):
        return reverse('home')