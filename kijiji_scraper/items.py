# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    date_listed = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    kilometers = scrapy.Field()
    used = scrapy.Field()
