from calendar import prmonth
import scrapy
from news_sites.normalize import clean_text
from news_sites.items import NewsSitesItem

class SenaSpider(scrapy.Spider): 
    name = "sena" 
    allowed_domains = ["sena.ir"] 
    start_urls = [ 
        "https://www.sena.ir/page/archive.xhtml?wide=0&ms=0&pi=1", 
    ]
    archive_pages = []

    def parse_page_content(self, response):
        item = NewsSitesItem()
        item['website'] = self.name
        item['title'] = clean_text(response.xpath('//h1[@class = "title"]/a/text()').get())
        try:
            item['published_datetime'] = clean_text(
            response.xpath('//div[@class="item-nav row"]/div[@class="col-xs-8 col-sm-5 item-date"]/span/text()').getall()[0]
            )
        except:
            item['published_datetime'] = ""
        item['body'] = \
            ' '.join(
                [   
                    clean_text(item)
                    for item in 
                    response.xpath(
                        ''' 
                            //div[@class = "item-text"]/p/text()|
                            //div[@class = "item-text"]/p/strong/text()
                        ''').getall()
                ]
            )
        item['tags'] = ','.join(
            [
                clean_text(item) for item in
                response.xpath('//div[@class = "item-boxes"]/section/div/ul/li/a/text()').getall()
            ]
        )
        item['link'] = response.request.url
        yield item

    def parse_archive_page(self, response):
        for link in response.xpath('//div[@class = "items"]/ul/li/div/h3/a/@href').getall():
            link = "https://" + self.name + ".ir" + link
            yield scrapy.Request(link, callback=self.parse_page_content)


    def parse(self, response):
        for i in range(1, 24, 1):
            url =  self.start_urls[0].replace("pi=1", "pi="+str(i))
            yield scrapy.Request(
                url,
                callback=self.parse_archive_page,
            )
