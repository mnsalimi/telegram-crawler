import scrapy
from news_sites.normalize import clean_text
from news_sites.items import NewsSitesItem

class NabzeBourseSpider(scrapy.Spider): 
    name = "nabzebourse" 
    allowed_domains = ["nabzebourse.com"] 
    start_urls = [ 
        "https://nabzebourse.com/fa/archive?service_id=&sec_id=&cat_id=&rpp=20&from_date=1397/12/01&to_date=1401/06/04&p=1", 
    ]
    def parse_page_content(self, response):
        item = NewsSitesItem()
        item['website'] = self.name
        item['title'] = clean_text(response.xpath('//title/text()').get())
        item['published_datetime'] = clean_text(
            response.xpath('//div[@class="news-body_top-tool_right"]/span/text()').getall()[0]
            )
        item['body'] = \
            ' '.join(
                [   
                    clean_text(item)
                    for item in 
                    response.xpath(
                        '''
                            //div[@class = "body"]/p/text()|
                            //div[@class = "body"]/p/a/text()|
                            //div[@class = "body"]/p/a/strong/text()|
                            //div[@class = "body"]/div/p/a/strong/text()|
                            //div[@class = "body"]/div/p/a/text()|
                            //div[@class = "body"]/div/p/text()
                        ''').getall()
                ]
            )
        item['tags'] = ','.join(
            [
                clean_text(item) for item in
                response.xpath('//div[@class = "tags-container"]/a/text()').getall()
            ]
        )
        item['link'] = response.request.url
        yield item

    def parse_archive_page(self, response):
        for link in response.xpath(
            '//div[@class = "archive_content"]/div[@class="last-news-art"]/a/@href'
            ).getall():
            link = "https://" + self.name + ".com" + link
            yield scrapy.Request(link, callback=self.parse_page_content)


    def parse(self, response):
        for i in range(1, 91, 1):
            url =  self.start_urls[0].replace("&p=1", "&p="+str(i))
            yield scrapy.Request(
                url,
                callback=self.parse_archive_page,
            )

            