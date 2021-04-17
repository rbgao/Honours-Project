import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = "help"
    start_urls = ["https://www.rba.gov.au/monetary-policy"]

    rules = (
        Rule(LinkExtractor(allow=(r'\/rba-board-minutes',)), callback = 'parse', follow= True),
    )
    
    def parse(self, response):
        yield {'Date': response.css('strong::text').extract()}
