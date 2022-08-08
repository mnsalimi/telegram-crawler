from email import message
from queue import PriorityQueue
from django.db import models
from django.core import serializers
from django.utils.html import mark_safe
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

# Create your models here.
class Post(models.Model):
    post_id = models.IntegerField()
    channel_id = models.IntegerField()
    channel_name = models.CharField(max_length=100, blank=True, null=True)
    datetime = models.DateTimeField()
    views = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=4096)
    symbols = models.CharField(max_length=4096, blank=True, null=True)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)

    @property
    def thumbnail_preview(self):
        if self.photo:
            _thumbnail = get_thumbnail(self.photo,
                                   '300x300',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            return format_html('<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, 300, 100))
        return ""