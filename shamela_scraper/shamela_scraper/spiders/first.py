# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FirstSpider(CrawlSpider):
    name = "first"
    allowed_domains = ['shamela.ws']
    start_urls = ['http://www.shamela.ws/index.php/categories']

    rules = [
            Rule(
                LinkExtractor(
                    #allow=['http:\/\/www\.shamela\.ws\/index.php\/book\/[0-9]*$']
                    allow=['.*']
                    #deny=['http:\/\/www\.shamela\.ws\/index.php\/book\/get_pdf\/[0-9]*$', 'http:\/\/www\.shamela\.ws\/browse.php\/.*$']
                    ),
                follow=False
                
                )
            ]

    #def parse(self, response):

         #pass


