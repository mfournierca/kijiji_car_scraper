import scrapy
import re
import itertools
from urlparse import urlparse

from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class BaseSpider(CrawlSpider):
    name = "base_spider"

    def _extract_domain(self, response):
        return urlparse(response.url).netloc

    def _clean_string(self, string):
        for i in [",", "\n", "\r", ";", ":", "\\"]:
            string = string.replace(i, "")
        return string.strip()

    def _extract_text_from_id(self, response, element, identifier):
        l = response.xpath("//{1}[@id='{0}']/.//text()".format(identifier, element)).extract()
        return self._clean_string(l[0]) if l else None

    def _extract_text_from_itemprop(self, response, element, identifier):
        l = response.xpath("//{1}[@itemprop='{0}']/.//text()".format(identifier, element)).extract()
        return self._clean_string(l[0]) if l else None

    def _extract_text_from_class(self, response, element, identifier):
        l = response.xpath("//{1}[contains(@class, '{0}')]".format(identifier, element)).extract()
        return l
