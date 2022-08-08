from django.contrib import admin
from crawler.models import Post
from django.utils.html import format_html
import os
from django.utils.html import mark_safe

class BookAdmin(admin.ModelAdmin):
    
    search_fields = ['message']
    list_per_page = 500
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True
    list_display= (
        'post_id',
        'channel_name',
        'datetime',
        'views',
        'message',
        'symbols',
        'sentiment',
        'photo',
        'thumbnail_preview'
    )
    readonly_fields = ('thumbnail_preview',)
    list_filter = [
        "channel_name",
        "symbols",
        "sentiment",
    ]
admin.site.register(Post, BookAdmin)
