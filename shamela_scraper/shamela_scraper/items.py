# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShamelaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   
    book_title = scrapy.Field()
    book_link = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()
    author_name = scrapy.Field()
