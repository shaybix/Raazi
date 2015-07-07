# -*- coding: utf-8 -*-
import scrapy


class FirstSpider(scrapy.Spider):
    name = "first"
    allowed_domains = ["shamela.ws"]
    start_urls = ('http://www.shamela.ws/')


    def parse(self, response):

        pass
