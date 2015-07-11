# -*- coding: utf-8 -*-


import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shamela_scraper.items import ShamelaScraperItem
import sys



class FirstSpider(CrawlSpider):
    name = "first"
    allowed_domains = ['shamela.ws']
    start_urls = ['http://www.shamela.ws/index.php/categories']

    rules = (
        Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*$',))), \
        Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*\/page-[0-9]*$',))), \
        Rule(LinkExtractor(allow=('\/index.php\/author\/[0-9]*$',)), callback='parse_items'), \
        Rule(LinkExtractor(allow=('\/index.php\/book\/[0-9]*$',)))
            )


    def parse_items(self, response):
        # print 'I am parsing'
        item = ShamelaScraperItem()
        book = {}
        books = []
        author = {}


        author['link'] = response.url


        died =  response.xpath('//table[@class="main_table"]/tr[2]/td[2]/text()').extract()
        died = ''.join(died)

        died = died.strip('\n\t').rstrip(' ').lstrip(' ')
        died = died.encode('utf-8')
        try:
            died = int(died)
            author['died'] = died

        except ValueError:
            author['died'] = None


        fullname =  response.xpath('//table[@class="main_table"]/tr[1]/td[2]/text()').extract()
        fullname = ''.join(fullname)
        author['fullname'] = fullname.strip('\n\t').rstrip(' ').lstrip(' ')

        name =  response.xpath('//h3[@class="contentTitle-h3"]/text()').extract()
        name = ''.join(name)
        author['name'] = name.strip('\n\t')


        # item['book_title'] =  sel.xpath('//td[@class="main_td"]/ol/li/a/text()').extract()
        # item['book_link'] = sel.xpath('//td[@class="main_td"]/ol/li/a/@href').extract()
        book_title = response.xpath('//td[@class="main_td"]/ol/li/a/text()').extract()
        book_link = response.xpath('//td[@class="main_td"]/ol/li/a/@href').extract()
        for title, link in zip(book_title, book_link):

            book['link'] = 'http://www.shamela.ws' + link
            book['title'] = title

            books.append(book)


        item['books'] = books
        item['author'] = author

        print item
        return  item


        #for sel in response.xpath('//td[@class="main_td"]/ol/li'):
         #   link = sel.xpath('//a/@href').extract()
          #  print link
