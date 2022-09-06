from scrapy.crawler import CrawlerProcess
from news_sites.spiders.boursepress import BoursePressSpider
from news_sites.spiders.nabzebourse import NabzeBourseSpider
from news_sites.spiders.sena import SenaSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

settings = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'result.csv',
        }
spiders_list = [
        BoursePressSpider,
        NabzeBourseSpider,
        SenaSpider,
    ]

def crawlesettingsr_process():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'result.csv'
    }) 
    for spider in spiders_list:
        process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'result.csv'
        }) 
        process.crawl(spider)
        process.start() # the script will block here until the crawling is finished
        # process.close()


def crawler_runner():
    runner = CrawlerRunner(
        settings
    )
    for spider in spiders_list:
        runner.crawl(spider)
        # runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    with open("result.csv", "r", encoding="utf-8") as f:
        results = f.readlines()
        header = results[0]
        results = [
                line.replace("\n", "").lstrip().rstrip().strip().split(",")
                for line in results[1:] if line!=header
            ]
        with open("result.csv", "w", encoding="utf-8") as f:
            f.write(header.rstrip().lstrip().strip().replace("\n", "")+"\n")
            for line in results:
                f.write(','.join(line)+"\n")

if __name__ == "__main__":
    # crawler_runner()
    mod = __import__("news_sites/spiders")
    for klass in vars(mod):
        o =  getattr(mod, klass)
        if type(o) == type:
            print(o)
        print(o)
