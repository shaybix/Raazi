# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shamela_crawler.items import ShamelaCrawlerItem
from scrapy.http import Request
import time  
global count


count = 1


class ShamelaSpider(CrawlSpider):
    name = "shamela"
    allowed_domains = ["shamela.ws"]
    start_urls = [
        'http://www.shamela.ws/index.php/categories/',
    
    ]

    rules = [
            Rule(LinkExtractor(
                allow=['http:\/\/www\.shamela\.ws\/index\.php\/category\/[0-9]*$']),
                callback='parse_category'),

            Rule(LinkExtractor(
                allow=['http:\/\/www\.shamela\.ws\/index\.php\/book\/[0-9]*$']))

    ]
    
    
        
    
    # TODO extract links for individual categories and
    # yield Request setting a callback
    
    def parse_category(self, response):
        #item = ShamelaCrawlerItem()
        global count
        links = response.xpath('//td[@class="regular-book"]/a/@href').re(r'/index.php/book/[0-9]*$')
        pagination = True if response.xpath('//div[@class="center"]/a/@href').extract() else None



        print '\n\n#################################################'
        print response.url
        print '#################################################\n'
        
        for link in links:

            url = 'http://www.shamela.ws' + link
            print '---------------' + str(count) + '---------------'
            print 'Book Url =====> ' + url 
            print 'Category =====> ' + str(response.url) + '\n\n'
            #return Request(url=url, callback=self.parse_category)
            count = count + 1


        if pagination is None:
            print 'NO NEXT PAGE AVAILABLE'
        else:
            go_to_page = response.xpath('//div[@class="center"]/a/@href').extract()[-2]
            last_page = response.xpath('//div[@class="center"]/a/@href').extract()[-1]


            print go_to_page 
            print last_page
            print 'NEXT PAGE AVAILABLE'    
    
        
        time.sleep(1)

 
    # TODO crawl and extract each book inside the category
    

