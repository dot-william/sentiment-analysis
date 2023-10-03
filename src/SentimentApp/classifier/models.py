from django.db import models

# Create your models here.
class SentimentFeature(models.Model):
    text = models.CharField(max_length=100)