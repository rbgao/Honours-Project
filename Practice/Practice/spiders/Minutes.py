import scrapy

class MinutesSpider(scrapy.Spider):
    name = "minutes"
    start_urls = ['https://www.rba.gov.au/monetary-policy/rba-board-minutes/2007',
                'https://www.rba.gov.au/monetary-policy/rba-board-minutes/2007']    
    def parse(self, response):
        yield {'link-suffix': response.css('u1 a::attr(href)').extract(),
                'Date': response.css('.list-articles a::text').extract()}