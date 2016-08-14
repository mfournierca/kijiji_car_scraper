import scrapy
import re
import itertools
from urlparse import urlparse

from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class AllCarSpider(CrawlSpider):
    name = "all_car_spider"
    spiders = [
        KijijiCarSpider(),
        OttawaHondaCarSpider()
    ]
    allowed_domains = list(itertools.chain.from_iterable([s.allowed_domains for s in spiders]))
    start_urls = list(itertools.chain.from_iterable([s.start_urls for s in spiders]))
    rules = list(itertools.chain.from_iterable([s.rules for s in spiders]))


class BaseCarSpider(CrawlSpider):
    name = "base_car_spider"

    def _extract_domain(self, response):
        return urlparse(response.url).netloc

    def _clean_string(self, string):
        for i in [",", "\n", "\r", ";", "\\"]:
            string = string.replace(i, "")
        return string.strip()


class KijijiCarSpider(BaseCarSpider):
    name = "kijiji_car_spider"
    allowed_domains = ["kijiji.ca"]
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


class OttawaHondaCarSpider(BaseCarSpider):
    name = "ottawahonad_car_spider"
    allowed_domains = ["ottawahonda.com"]
    start_urls = [
        "https://www.ottawahonda.com/used/search.html"
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "https://www.ottawahonda.com/used/.+"
                ]
            ),
            callback='parse_ottawahonda_item'
        ),
        Rule(
            LinkExtractor(
                allow=["https://www.ottawahonda.com/used/search.html?spage=[0-9]"]
            )
        )
    ]

    def parse_ottawahonda_item(self, respons):
        car = items.CarItem()
        car["url"] = response.url
        car["domain"] = self._extract_domain(response)

