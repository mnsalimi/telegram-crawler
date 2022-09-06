import scrapy
from news_sites.normalize import clean_text
from news_sites.items import NewsSitesItem


class BoursePressSpider(scrapy.Spider): 

    name = "boursepress" 
    allowed_domains = ["boursepress.ir"] 
    start_urls = [ 
        "https://boursepress.ir/page/archive?category=-1&newstype=-1&fromday=11&frommonth=10&fromyear=1278&today=3&tomonth=6&toyear=1401&count=20&p=1", 
    ]

    def parse_page_content(self, response):
        item = NewsSitesItem()
        item['website'] = self.name
        item['title'] = clean_text(response.xpath('//title/text()').get())
        item['published_datetime'] = clean_text(
            response.xpath('//div[@class="news-map"]/div/text()').getall()[1]
            )
        item['body'] = \
            ' '.join(
                [   clean_text(item)
                    for item in 
                    response.xpath('//div[@class = "news-text"]/p/text()|//div[@class = "news-text"]/p/a/text()').getall()
                ]
            )
        item['tags'] = ','.join(
            [
                clean_text(item) for item in
                response.xpath('//div[@class = "tags-content"]/a/text()').getall()
            ]
        )
        item['link'] = response.request.url
        yield item

    def parse_archive_page(self, response):
        for link in response.xpath(
            '//ul[@class = "news-list-t"]/li/a/@href'
            ).getall():
            yield scrapy.Request(link, callback=self.parse_page_content)

    def parse(self, response):
        for i in range(1, 600, 1):
            url =  self.start_urls[0].replace("&p=1", "&p="+str(i))
            yield scrapy.Request(
                url,
                callback=self.parse_archive_page,
            )
