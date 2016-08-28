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


class FuelRatingItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    lphkm_city = scrapy.Field() # Litres Per Hecta-Kilometer, L / 100km
    lphkm_hwy = scrapy.Field()
    estimated_fuel_cost_year = scrapy.Field()
    model_class = scrapy.Field()
    engine_size_litres = scrapy.Field()
    cylinders = scrapy.Field()
    transmission = scrapy.Field()
    fuel = scrapy.Field()
    ranking_class = scrapy.Field()
    ranking_overall = scrapy.Field()

