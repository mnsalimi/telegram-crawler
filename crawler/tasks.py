from __future__ import absolute_import, unicode_literals
from turtle import pos
from celery import shared_task
from .models import Post 
from .crawler_pipeline import CrawlerpPipeline
from .documents import PostDocument
import datetime

telegram_cralwer = CrawlerpPipeline()

@shared_task()
def crawl_telegram_channel_peridcially():
    res_crawled = telegram_cralwer.crawl_channel()
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
                views = res['views'],
                message = res['message'],
                symbols = res['symbols'],
                sentiment = res['sentiment'],
                photo = res.get('photo', None)
            )
            post.save()

def crawl_telegram_channel(limit_datetime=None):
    count = 0
    for res in telegram_cralwer.crawl_channel(limit_datetime=limit_datetime):
        if not res:
            continue
        if res.get("message", None) is None:
            continue

        count += 1
        if count%50 == 0:
            print("count: ", str(count))
        doc_founded = False
        try:
            res_docs = PostDocument.search().query("match", post_id=res["post_id"])
            for _ in res_docs:
                doc_founded = True
                break
        except:
            pass
        if not doc_founded:
            post = Post(
                post_id = res['post_id'],
                channel_id = res['channel_id'],
                channel_name = res['channel_name'],
                datetime = res['datetime'],
                views = res['views'],
                message = res['message'],
                symbols = res['symbols'],
                sentiment = res['sentiment'],
                photo = res.get('photo', None)
            )
            post.save()