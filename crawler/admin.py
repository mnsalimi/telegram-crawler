from django.contrib import admin
from crawler.models import Post
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display= (
        'post_id',
        'channel_id',
        'datetime',
        'message',
        'views',
    )

  
admin.site.register(Post, BookAdmin)
