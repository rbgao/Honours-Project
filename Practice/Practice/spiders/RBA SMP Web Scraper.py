import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from html_stripper import strip_tags

class MySpider(CrawlSpider):
    name = "SMPscraper"
    start_urls = ["https://www.rba.gov.au/publications/smp/",
                    "https://www.rba.gov.au/publications/smp/2021/feb/"]
    rules = (
            Rule(LinkExtractor(allow=(r'https:\/\/www.rba.gov.au\/publications\/smp\/\d+\/.*',)), callback = 'parse', follow= True),
        )
    
    def parse(self, response):
        
        url = response.request.url
        
        if re.search(r'https:\/\/www.rba.gov.au\/publications\/smp\/\d+\/\w+\/[^g].*.html', url):
            
            Date =  response.css('span.publication-name::text').extract()

            cleaned_date = []

            for date in Date:
                cleaned_date.append(strip_tags(date.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' '))) 

            Section = response.css('h1.page-title::text').extract()

            cleaned_section = []

            for section in Section:
                cleaned_section.append(strip_tags(section.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' '))) 
            
            cleantext = []
            text = response.xpath('//div[@id="content"]/p').extract()
            
            for paragraph in text:
                cleantext.append(strip_tags(paragraph.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ')))

            dotpoints = response.xpath('//div[@id="content"]//li[not(ancestor::div/@class="nav-publication-contents")]').extract()

            for point in dotpoints:
                cleantext.append(strip_tags(point.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ')))

            if re.search(r'https:\/\/www.rba.gov.au\/publications\/smp\/\d+\/\w+\/[^gfc].*.html', url):
                yield { 'Date': cleaned_date, 
                        'Section':cleaned_section, 
                        'Text': cleantext, 
                        'URL': response.request.url,  
                        }

