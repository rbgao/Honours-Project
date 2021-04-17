import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

#selector = Selector(text=HTML)

class MySpider(CrawlSpider):
    name = "helpME"
    start_urls = [  "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2006/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2007/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2008/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2009/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2010/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2011/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2012/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2013/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2014/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2015/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2016/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2017/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2018/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2019/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2020/",
                    "https://www.rba.gov.au/monetary-policy/rba-board-minutes/2021/",
                   ]

    rules = (
            Rule(LinkExtractor(allow=(r'\/rba-board-minutes\/\d+\/\d\d\d\d-\d\d-\d\d.html',)), callback = 'parse', follow= True),
            Rule(LinkExtractor(allow=(r'\/rba-board-minutes\/\d+\/\d+.html',)), callback = 'parse', follow= True),
        )
    
    def parse(self, response):
        item = {}
        for cnt, h2 in enumerate(response.css('section > h2'), start=1):
            sectiontitles = h2.xpath('normalize-space()').get()
            sectiontext = h2.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt).getall()
            sectiontext_cleaned = []
            for paragraph in sectiontext:
                sectiontext_cleaned.append(paragraph.replace('\r',' ').replace('\n','').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
            item[sectiontitles] = sectiontext_cleaned
        for cnt_1, h2_1 in enumerate(response.css('div#content.column-content.content-style > h2'), start = 1):
            sectiontitles = h2_1.xpath('normalize-space()').get()
            sectiontext = h2_1.xpath('following-sibling::p[count(preceding-sibling::h2)=$cnt]', cnt=cnt_1).getall()
            sectiontext_cleaned = []
            for paragraph in sectiontext:
                sectiontext_cleaned.append(paragraph.replace('\r',' ').replace('\n','').replace('\t','').replace('\xa0',' ').replace('<p>','').replace('</p>',''))
            item[sectiontitles] = sectiontext_cleaned
        yield { 'Date': response.css('strong::text').extract(), 
                 'Text' : item,
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
    