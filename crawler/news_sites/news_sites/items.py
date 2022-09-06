# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSitesItem(scrapy.Item):
    website = scrapy.Field()
    title = scrapy.Field()
    published_datetime = scrapy.Field()
    body = scrapy.Field()
    views = scrapy.Field()
    tags = scrapy.Field()
    link = scrapy.Field()