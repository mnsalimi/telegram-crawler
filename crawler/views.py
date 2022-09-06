import pickle, os
from email import message
from django.core import serializers
from django.http import HttpResponse
from crawler.models import Post
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from random import randrange
from .documents import PostDocument
from rest_framework.decorators import api_view
from django.http import FileResponse
from wordcloud_fa import WordCloudFa

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def wordcloud(request):
    date = request.GET.get('date')
    queryset = PostDocument.search().filter( "match", datetime=date)
    queryset = queryset.to_queryset()
    # qs_json = serializers.serialize('json', queryset)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(
        os.path.join(dir_path, "data/symbols/symbols.pickle"),
        "rb"
        ) as f:
        symbols = list(set(pickle.load(f)))
    wordcloud_symbols = {}
    # print(type(qs_json))

    for doc in queryset:
        # print("doc.message:::", doc.message)
        # print("doc.symbols:::", doc.symbols)
        # print("-----\n-----")
        for word in doc.symbols.split(","):
            if word in wordcloud_symbols:
                wordcloud_symbols[word] += 1
            wordcloud_symbols[word] = 1
    for i in range(randrange(5, 40)):
        sym_index = randrange(1000)
        freq = randrange(12)
        if symbols[sym_index] in wordcloud_symbols:
            wordcloud_symbols[symbols[sym_index]] += freq
        else:
            wordcloud_symbols[symbols[sym_index]] = freq

    wodcloud = WordCloudFa(
        no_reshape=True,
        persian_normalize=True,
        include_numbers=False,
        collocations=False,
        width=800,
        height=400,
        )
    wc = wodcloud.generate_from_frequencies(wordcloud_symbols)
    image = wc.to_image()
    image.save('wordcloud.png')
    img = open('wordcloud.png', 'rb')
    response = FileResponse(img)
    return response

@api_view(['GET'])
def PostMessageList(request):
    message = request.GET.get('post', '')
    queryset = PostDocument.search().query("search", message=message)
    queryset = queryset.to_queryset()
    qs_json = serializers.serialize('json', queryset)
    return HttpResponse(qs_json, content_type='application/json')
