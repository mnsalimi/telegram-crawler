from email import message
from django.db import models
from django.core import serializers

# Create your models here.
class Post(models.Model):
    post_id = models.IntegerField()
    channel_id = models.IntegerField()
    datetime = models.DateTimeField()
    message = models.CharField(max_length=4096)
    views = models.IntegerField()
