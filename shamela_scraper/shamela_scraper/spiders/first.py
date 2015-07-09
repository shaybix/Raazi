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
        Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*$',))), \
        Rule(LinkExtractor(allow=('\/index.php\/category\/[0-9]*\/page-[0-9]*$',))), \
        Rule(LinkExtractor(allow=('\/index.php\/author\/[0-9]*$',)), callback='parse_items'), \
        Rule(LinkExtractor(allow=('\/index.php\/book\/[0-9]*$',)))
            )


    def parse_items(self, response):
        # print 'I am parsing'
        item = ShamelaScraperItem()
        item['author_name'] = response.xpath('//h3[@class="contentTitle-h3"]/text()').extract()
        item['author_link'] = response.url


        for sel in response.xpath('//td[@class="main_td"]/ol/li'):
            # item['book_title'] = sel.xpath('//td[@class="main_td"]/ol/li/a/text()').extract()
            # item['book_link'] = sel.xpath('//td[@class="main_td"]/ol/li/a/@href').extract()
            item['book'] = 


        return  item

        #for sel in response.xpath('//td[@class="main_td"]/ol/li'):
         #   link = sel.xpath('//a/@href').extract()
          #  print link
