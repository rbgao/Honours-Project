import scrapy

class PostSpider(scrapy.Spider):
    name = "quotes"
    
    start_urls = [
        'https://www.rba.gov.au/monetary-policy/rba-board-minutes/2021/'
    ]
