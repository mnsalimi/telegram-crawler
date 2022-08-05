from rest_framework import serializers
from crawler.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('post_id', 'channel_id', 'datetime', 'message', 'views')