import scrapy
import re
import itertools
from urlparse import urlparse

from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from BaseSpider import BaseSpider


class KijijiCarSpider(BaseSpider):
    name = "kijiji_car_spider"
    allowed_domains = [
        "kijiji.ca"
    ]
    start_urls = [
        "http://www.kijiji.ca/b-cars-trucks/ottawa/c174l1700185",
        "http://www.kijiji.ca/b-cars-trucks/ottawa/suv+crossover/c174l1700185a138",
        "http://www.kijiji.ca/b-cars-trucks/ottawa/mini+van/c174l1700185a138"
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "http://www.kijiji.ca/v-cars-trucks/ottawa/.+"
                ]
            ),
            callback='parse_item'
        ),
        Rule(

            LinkExtractor(
                allow=["http://www.kijiji.ca/b-cars-trucks/ottawa/.*?/page-[0-9]/.+"]
            )
        )
    ]

    def parse_item(self, response):
        car = items.CarItem()
        car["url"] = response.url
        car["domain"] = self._extract_domain(response)
        car["price"] = self._extract_field(response, "Price")
        car["date_listed"] = self._extract_field(response, "Date Listed")
        car["title"] = self._extract_title(response)
        car["description"] = self._extract_description(response)
        car["make"] = self._extract_link_field(response, "Make")
        car["model"] = self._extract_link_field(response, "Model")
        car["year"] = self._extract_field(response, "Year")
        car["kilometers"] = self._extract_field(response, "Kilometers")
        return car

    def _extract_title(self, response):
        l = " ".join(response.xpath("//h1/text()").extract())
        return self._clean_string(l)

    def _extract_description(self, response):
        l = " ".join(response.xpath("//span[@itemprop='description']/text()").extract())
        return self._clean_string(l)

    def _extract_field(self, response, fieldname):
        l = response.xpath("//th[contains(text(), '{0}')]/following::td[1]//./text()".
                format(fieldname)).extract()
        return l[0].strip() if l else None

    def _extract_link_field(self, response, fieldname):
        l = response.xpath("//th[contains(text(), '{0}')]/following::td[1]/a/span/./text()".
                format(fieldname)).extract()
        return l[0].strip() if l else None

    def _extract_bedrooms(self, response):
        r = re.search(r'kijiji.ca\/v-(\d)-bedroom-apartments-condos', response.url)
        return r.group(1).strip() if r else None


class TonyGrahamToyotaCarSpider(BaseCarSpider):
    name = "tonygrahamtoyota_car_spider"
    allowed_domains = [
        "www.tonygrahamtoyota.com",
        "tonygrahamtoyota.com"
    ]
    start_urls = [
        "http://www.tonygrahamtoyota.com/all/"
        "http://www.tonygrahamtoyota.com/all/keywords/",
    ] + [
        "http://www.tonygrahamtoyota.com/all/s/year/o/desc/pg/{0}".format(i) for i in range(10)
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "http://www.tonygrahamtoyota.com/all/vehicle/.*"
                ]
            ),
            callback="parse_item"
        ),
        Rule(
            LinkExtractor(
                allow=[
                    "http://www.tonygrahamtoyota.com/all/s/year/o/desc/pg/[0-5]"
                ]
            )
        )
    ]

    def parse_item(self, response):
        car = items.CarItem()
        car["url"] = response.url
        car["domain"] = self._extract_domain(response)
        car["price"] = self._extract_text_from_id(response, "span", "final-price")
        car["year"] = self._extract_text_from_itemprop(response, "span", "releaseDate")
        car["make"] = self._extract_text_from_itemprop(response, "span", "brand")
        car["model"] = self._extract_text_from_itemprop(response, "span", "model")
        car["kilometers"] = self._extract_kilometers(response)
        car["description"] = self.self._extract_text_from_id(response, "div", "collapseVehicleDetails")
        return car

    def _extract_kilometers(self, response):
        l = self._extract_text_from_itemprop(response, "td", "mileageFromOdometer")
        return l.replace("km", "") if l else None


class JimTubmanCarSpider(BaseCarSpider):
    name = "jimtubman_car_spider"
    allowed_domains = [
        "www.tubmanchev.com"
    ]
    start_urls = [
        "http://www.tubmanchev.com/used/",
        "http://www.tubmanchev.com/new/"
    ] + [
        "http://www.tubmanchev.com/used/s/year/o/desc/pg/{0}".format(i)
        for i in range(10)
    ] + [
        "http://www.tubmanchev.com/used/s/year/o/desc/pg/{0}".format(i)
        for i in range(10)
    ]

    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "http://www.tubmanchev.com/used/vehicle/.*"
                ]
            ),
            callback="parse_item"
        )
    ]

    def parse_item(self, response):
        car = items.CarItem()
        car["url"] = response.url
        car["domain"] = self._extract_domain(response)
        car["model"] = self._extract_text_from_itemprop(response, "span", "model")
        car["title"] = self._extract_text_from_itemprop(response, "h1", "name")
        car["price"] = self._extract_text_from_itemprop(response, "span", "price")
        car["kilometers"] = self._extract_text_from_itemprop(response, "span", "mileageFromOdometer")
        car["year"] = self._extract_text_from_itemprop(response, "span", "releaseDate")
        car["make"] = self._extract_text_from_itemprop(response, "span", "manufacturer")
        car["description"] = self._extract_text_from_itemprop(response, "span", "description")
        return car


class OttawaHondaCarSpider(BaseCarSpider):
    name = "ottawahonda_car_spider"
    allowed_domains = [
        "ottawahonda.com"
    ]
    start_urls = [
        "https://www.ottawahonda.com/used/search.html"
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "https://www.ottawahonda.com/used/.+id\d+"
                ]
            ),
            callback='parse_item'
        ),
        Rule(
            LinkExtractor(
                allow=["https://www.ottawahonda.com/used/search.html?spage=[0-9]"]
            )
        )
    ]

    def parse_item(self, response):
        car = items.CarItem()
        car["url"] = response.url
        car["domain"] = self._extract_domain(response)
        car["model"] = self._extract_field(response, "Model")
        car["title"] = self._extract_title(response)
        car["price"] = self._extract_field(response, "Price")
        car["kilometers"] = self._extract_kilometers(response)
        car["year"] = self._extract_year(response)
        car["make"] = self._extract_make(response)
        return car

    def _extract_make(self, response):
        title = self._extract_title(response)
        m = re.search('^\s*(\d+)\s*(\w+).*', title)
        l = m.group(2)
        return self._clean_string(l) if l else None

    def _extract_year(self, response):
        title = self._extract_title(response)
        m = re.search('^\s*(\d+).*', title)
        l = m.group(1)
        return self._clean_string(l) if l else None

    def _extract_kilometers(self, response):
        l = response.xpath("//div[@id='carPrice']/span[2]/text()").extract()
        l = self._clean_string(l[0]).replace("(", "").replace(")", "").replace("km", "") if l else None
        return l

    def _extract_title(self, response):
        l = response.xpath("//h1[@id='carTitle']/text()").extract()
        return self._clean_string(l[0]) if l else None

    def _extract_field(self, response, fieldname):
        l = response.xpath("//li/span[contains(text(), '{0}: ')]/./text()".format(fieldname)).extract()
        return self._clean_string(l[0]).replace(fieldname, "") if l else None
