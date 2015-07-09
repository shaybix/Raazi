# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shamela_scraper.items import ShamelaScraperItem



class FirstSpider(CrawlSpider):
    name = "first"
    allowed_domains = ['shamela.ws']
    start_urls = ['http://www.shamela.ws/index.php/categories']

    rules = (
            Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*$)',))), \
            Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*\/page-[0-9]*$',))), \
            
            Rule(LinkExtractor(allow=('\/index.php\/book\/[0-9]*$',)), callback='parse_items')
            )

   
    def parse_items(self, response):
        print 'I am parsing'
        #item = ShamelaScraperItem()
        #item['book_title'] = response.xpath('//h3[@class="contentTitle-h3"]/text()').extract()
        #item['book_link'] = response.url
        
        #return  item

        #for sel in response.xpath('//td[@class="main_td"]/ol/li'):
         #   link = sel.xpath('//a/@href').extract()
          #  print link


