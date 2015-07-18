# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shamela_crawler.items import ShamelaCrawlerItem, BookItem, AuthorItem
from scrapy.http import Request
import time 
import re

global count
global parsed



count = 1
parsed = []




class ShamelaSpider(CrawlSpider):
    name = "shamela"
    allowed_domains = ["shamela.ws"]
    start_urls = [
        'http://www.shamela.ws/index.php/categories/',
    
    ]

    rules = [
            Rule(LinkExtractor(
                allow=['http:\/\/www\.shamela\.ws\/index\.php\/category\/[0-9]*$']),
                callback='parse_category_page'),

            Rule(LinkExtractor(
                allow=['http:\/\/www\.shamela\.ws\/index\.php\/book\/[0-9]*$']))

    ]
    
    
        
    
    # TODO extract links for individual categories and
    # yield Request setting a callback
    
    def parse_category_page(self, response):
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
            yield Request(url=url, callback=self.parse_book_page)
            count = count + 1


        if pagination is None:
            print 'NO NEXT PAGE AVAILABLE'
        else:
            current_page = response.url
            go_to_page = 'http://www.shamela.ws' + response.xpath('//div[@class="center"]/a/@href').extract()[-2]
            last_page = 'http://www.shamela.ws' + response.xpath('//div[@class="center"]/a/@href').extract()[-1]
            next_page_number = int(go_to_page.split('-')[-1])
            
            print "JUST SCRAPED ========> [" + current_page + "]"
            
            
            if current_page not in parsed and next_page_number != 1:

                yield Request(url=go_to_page, callback=self.parse_category_page)
             
            parsed.append(current_page)

 
    # TODO crawl and extract each book inside the category
    # FIXME ensure books are nested in an author's books field


    def parse_book_page(self, response):

        Book = BookItem()
        links = {}
        Book['title'] = response.xpath('//*[@id="content"]/div[2]/span[1]/span[2]/text()').extract()[0]
        Book['publisher'] = response.xpath('//*[@id="content"]/div[2]/span[4]/span[2]/text()').extract()[0]

        
        urls  = response.xpath('//div[@id="content"]/div[3]/a/@href').extract()
        
        for url in urls:
        
            if url.split('.')[-1] == 'rar':
                links['Bok'] = url
            
            elif url.split('.')[-1] == 'epub':
                links['Epub'] = url
            
            elif re.search('waqfeya', url):
            
                links['Pdf'] = url
                
        
        Book['links'] = links
        
        print Book
        
        time.sleep(2)


        #download_link = response.xpath('//a/@href').re(r'http://shamela.ws/books/[0-9]*/[0-9]*.rar$')
        
        #print  download_link
        #print 'i am inside the page of the BOOK!'




    def parse_author_page():
        pass
    

