from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.PostList.as_view()),
    path('get-posts', views.PostMessageList),
    path('wordcloud', views.wordcloud),
]
