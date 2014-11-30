# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GroceryItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    ASIN = scrapy.Field()
    bigImage = scrapy.Field()
    url = scrapy.Field()
    pass
