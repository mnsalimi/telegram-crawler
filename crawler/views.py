from email import message
from django.core import serializers
from django.http import HttpResponse
from crawler.models import Post
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from .documents import PostDocument
from rest_framework.decorators import api_view


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['GET'])
def PostMessageList(request):
    message = request.GET.get('post', '')
    queryset = PostDocument.search().query("match", message=message)
    queryset = queryset.to_queryset()
    qs_json = serializers.serialize('json', queryset)
    return HttpResponse(qs_json, content_type='application/json')
