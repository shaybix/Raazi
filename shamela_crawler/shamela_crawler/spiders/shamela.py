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
        'http://www.shamela.ws',
    
    ]

    rules = [
            Rule(LinkExtractor(
                allow=['http:\/\/www\.shamela\.ws\/index\.php\/author\/[0-9]*$']),
                callback='parse_author_page',
                follow=True),

            #Rule(LinkExtractor(
            #    allow=['http:\/\/www\.shamela\.ws\/index\.php\/book\/[0-9]*$']))

    ]
    
    
        
    
    # TODO extract author pages and callback to parse_author_page
    
    
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
            pass
        else:
            current_page = response.url
            go_to_page = 'http://www.shamela.ws' + response.xpath('//div[@class="center"]/a/@href').extract()[-2]
            last_page = 'http://www.shamela.ws' + response.xpath('//div[@class="center"]/a/@href').extract()[-1]
            next_page_number = int(go_to_page.split('-')[-1])
            
            
            if current_page not in parsed and next_page_number != 1:

                yield Request(url=go_to_page, callback=self.parse_category_page)
             
            parsed.append(current_page)

 
    
    # TODO ensure books are nested in an author's books field


    def parse_book_page(self, response):

        Book = BookItem()
        links = {}
        Book['title'] = response.xpath('//*[@id="content"]/div[2]/span[1]/span[2]/text()').extract()[0]
        Book['publisher'] = response.xpath('//*[@id="content"]/div[2]/span[4]/span[2]/text()').extract()[0]

        # TODO take author's url and yield Request
        author_url  = response.xpath('//*[@class="contentTitle-h3"]/span/a/@href').extract()[0].encode('utf-8')
        author_url = 'http://www.shamela.ws' + author_url
        

       


        urls  = response.xpath('//div[@id="content"]/div[3]/a/@href').extract()
        
        for url in urls:
        
            if url.split('.')[-1] == 'rar':
                links['Bok'] = url
            
            elif url.split('.')[-1] == 'epub':
                links['Epub'] = url
            
            elif re.search('waqfeya', url):
            
                links['Pdf'] = url
                
        
        Book['links'] = links
        
        
        request = Request(url=author_url, callback=self.parse_author_page) 

        request.meta['book'] = Book
        
        return request


    def parse_author_page(self, response):
        books = BookItem()

        found_books = response.xpath('//div[@id="content"]/table/tr[4]/td[2]/ol/li/a')
        
        #print found_books 
        #time.sleep(4)
        books['books'] = []
        book = {}
        

        # FIXME the loop returns same data for each cycle creating duplicates

        for each in found_books:
        
            book['link'] = 'http://www.shamela.ws' + each.xpath('@href').extract()[0]
            book['title'] = each.xpath('text()').extract()[0]
            
            books['books'].append(book)

        print books
        time.sleep(3)

        
        Author = AuthorItem()

        Author['books'] = books
        

        Author['link'] = response.url


        Author['died'] = response.xpath('//div[@id="content"]/table/tr[2]/td[2]/text()').extract()[0]

        Author['full_name'] = response.xpath('//div[@id="content"]/table/tr[1]/td[2]/text()').extract()[0]
        
        #return Author


    
