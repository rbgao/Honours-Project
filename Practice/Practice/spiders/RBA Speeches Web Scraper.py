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
    
 #  def parse(self, response):
 #      item = {}
 #      Speaker = response.css('strong.rss-speech-speaker::text').getall()
 #      for cnt, h2 in enumerate(response.css('section > h2'), start=1):
 #          sectiontitles = h2.xpath('normalize-space()').get()
 #          sectiontext = h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall()
 #          sectiontext_cleaned = []
 #          for paragraph in sectiontext:
 #              sectiontext_cleaned.append(paragraph.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
 #          item[sectiontitles] = sectiontext_cleaned
 #      for cnt_1, h2_1 in enumerate(response.css('div#content.column-content.content-style >h2'), start = 1):
 #          sectiontitles = h2_1.xpath('normalize-space()').get()
 #          sectiontext = h2_1.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt_1).getall()
 #          sectiontext_cleaned = []
 #          for paragraph in sectiontext:
 #              sectiontext_cleaned.append(paragraph.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
 #          item[sectiontitles] = sectiontext_cleaned
 #      url = response.request.url
 #      if re.search(r'https:\/\/www.rba.gov.au\/speeches\/\d+\/sp.*\d.html', url):
 #          yield { 'Date': response.xpath('//time/@datetime').extract(), 
 #                  'Speaker': response.css('strong.rss-speech-speaker::text').extract(),
 #                  'Text' : item,
 #                  'URL': response.request.url ,
 #                  'Position': response.css('span.rss-speech-position::text').extract()  
 #                  }

    def parse(self, response):
        item = {}
        Speaker = response.css('strong.rss-speech-speaker::text').getall()
        #text = response.xpath('//div[@id ="content"]/descendant::text()[not(ancestor::div/@class="references")][not(ancestor::div/@class="footnotes")][not(ancestor::div/@class="bibliography")][not(ancestor::div/@class="js-page-header")]').extract()
        cleantext = []
        text = response.xpath('//div[@id="content"]/p').extract()
        for paragraph in text:
            cleantext.append(paragraph.replace('\r','').replace('\n',' ').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
        dotpoints = response.css('div#content.column-content.content-style li::text').extract()
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
# The following code is used for scrapy shell:

    # For Section:
        #for cnt, h2 in enumerate(response.css('section > h2'), start = 1):
            #print(h2.xpath('normalize-space()').get())
            #print(h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall())

    #For Div class:
        #for cnt, h2 in enumerate(response.css('div#content.column-content.content-style > h2'), start = 1):
        #     print(h2.xpath('normalize-space()').get())
        #       print(h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall())

# Version 1:
#def parse(self, response):
#        item = {}
#        for cnt, h2 in enumerate(response.css('section > h2'), start=1):
#            sectiontitles = h2.xpath('normalize-space()').get()
#            sectiontext = h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall()
#            item[sectiontitles] = sectiontext
#        for cnt_1, h2_1 in enumerate(response.css('div#content.column-content.content-style > h2'), start = 1):
#            sectiontitles = h2_1.xpath('normalize-space()').get()
#            sectiontext = h2_1.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt_1).getall()
#            item[sectiontitles] = sectiontext
#        yield { 'Date': response.css('strong::text').extract(), 
#                 'Text' : item,
#            }


# Testing automatic cleaning
 #For Section:
 #       for cnt, h2 in enumerate(response.css('section > h2'), start = 1):
 #           print(h2.xpath('normalize-space()').get())
 #           sectiontext = h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall()
 #           sectiontext_cleaned = []
 #           for paragraph in sectiontext:
 #               sectiontext_cleaned.append(paragraph.replace('\r',' ').replace('\n','').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
 #           print(sectiontext_cleaned)
    