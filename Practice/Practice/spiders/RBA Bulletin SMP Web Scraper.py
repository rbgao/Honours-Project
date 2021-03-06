import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from html_stripper import strip_tags

#selector = Selector(text=HTML)

class MySpider(CrawlSpider):
    name = "SMPscraper_bulletin"
    start_urls = ["https://www.rba.gov.au/publications/bulletin/"]
    rules = (
            Rule(LinkExtractor(allow=(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/\d+\/.*',)), callback = 'parse', follow= True) ,
        )
    
    def parse(self, response):
        
        url = response.request.url
        
        if re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/200[0-5]\/[fman]\w[^r]\/1.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/199[7-9]\/[fman][^p][^r]\/1.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/1997\/nov\/2.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/1998\/may\/2.html', url):
            
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

            dotpoints = response.xpath('//div[@id="content"]//li[not(ancestor::div/@class="nav-page-contents")]').extract() 

            for point in dotpoints:
                cleantext.append(strip_tags(point.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ')))

            boxtext = response.xpath('//div[@class="box-info"]/p').extract()

            for text in boxtext:
                cleantext.append(strip_tags(text.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ')))

            if re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/200[0-5]\/[fman]\w[^r]\/1.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/199[7-9]\/[fman][^p][^r]\/1.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/1997\/nov\/2.html', url) or re.search(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/1998\/may\/2.html', url):
                yield { 'Date': cleaned_date, 
                        'Section':cleaned_section, 
                        'Text': cleantext, 
                        'URL': response.request.url,  
                        }