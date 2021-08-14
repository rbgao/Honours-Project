import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

#selector = Selector(text=HTML)

class MySpider(CrawlSpider):
    name = "speechesscraper"
    start_urls = ["https://www.rba.gov.au/speeches/"] 
                
    rules = (
           Rule(LinkExtractor(allow=(r'https:\/\/www.rba.gov.au\/speeches\/\d+\/.*',)), callback = 'parse', follow= True),
        )
    
    def parse(self, response):
        item = {}
        Speaker = response.css('strong.rss-speech-speaker::text').getall()
        #text = response.xpath('//div[@id ="content"]/descendant::text()[not(ancestor::div/@class="references")][not(ancestor::div/@class="footnotes")][not(ancestor::div/@class="bibliography")][not(ancestor::div/@class="js-page-header")]').extract()
        cleantext = []
        text = response.xpath('//div[@id="content"]/p').extract()
        for paragraph in text:
            cleantext.append(paragraph.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
        
        dotpoints = response.xpath('//div[@id="content"]//li[not(ancestor::ul/@class="links")]').extract()
        for point in dotpoints:
            cleantext.append(point.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))

        url = response.request.url
        if re.search(r'https:\/\/www.rba.gov.au\/speeches\/\d+\/sp.*\d.html', url):
            yield { 'Date': response.xpath('//time/@datetime').extract(), 
                    'Speaker': response.css('strong.rss-speech-speaker::text').extract(),
                    'Text' : cleantext, 
                    'URL': response.request.url ,
                    'Position': response.css('span.rss-speech-position::text').extract()  
                    }
