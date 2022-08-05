from __future__ import absolute_import, unicode_literals
from turtle import pos
from celery import shared_task
from .models import Post 
from .telegram_cralwer import TelegramCrawler
from .documents import PostDocument

telegram_cralwer = TelegramCrawler()

@shared_task()
def crawle_telegram_channel():
    res_crawled = telegram_cralwer.crawle_channel()
    for res in res_crawled:
        res_docs = PostDocument.search().query("match", post_id=res["post_id"])
        doc_founded = False
        for _ in res_docs:
            doc_founded = True
            break
        if not doc_founded:
            post = Post(
                post_id = res['post_id'],
                channel_id = res['channel_id'],
                datetime = res['datetime'],
                message = res['message'],
                views = res['views'],
            )
            post.save()
            with open("crawler/tellllll.txt", "a", encoding="utf-8") as f:
                f.write(str(post)+"\n")