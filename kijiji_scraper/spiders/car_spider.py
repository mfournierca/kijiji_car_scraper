import scrapy
import re
from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class KijijiCarSpider(CrawlSpider):
    name = "kijiji_car_spider"
    allowed_domains = ["kijiji.ca"]
    start_urls = ["http://www.kijiji.ca/b-apartments-condos/ottawa/c37l1700185"]
    rules = [
        Rule(
            LinkExtractor(
                allow=["http://www.kijiji.ca/b-cars-trucks/ottawa/.+"]
            ),
            callback='parse_item'),
        Rule(
            LinkExtractor(
                allow=["http://www.kijiji.ca/b-cars-trucks/ottawa/.*?/page-[0-10]/.+"]
            )
        )
    ]

    def parse_item(self, response):
        car = items.CarItem()

        car["url"] = response.url
        car["price"] = self._extract_field(response, "Price")
        car["date_listed"] = self._extract_field(response, "Date Listed")
        car["title"] = self._extract_title(response)
        car["description"] = self._extract_description(response)
        car["make"] = self._extract_field(response, "Make")
        car["model"] = self._extract_field(response, "Model")
        car["year"] = self._extract_field(response, "Year")
        car["kilometers"] = self._extract_field(response, "Kilometers")

        return car

    def _clean_string(self, string):
        for i in [",", "\n", "\r", ";", "\\"]:
            string = string.replace(i, "")
        return string.strip()

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

    def _extract_bedrooms(self, response):
        r = re.search(r'kijiji.ca\/v-(\d)-bedroom-apartments-condos', response.url)
        return r.group(1).strip() if r else None


class KijijiCarSUVSpider(KijijiCarSpider):
    name = "kijiji_car_suv_spider"
    start_urls = ["http://www.kijiji.ca/b-cars-trucks/ottawa/suv+crossover/c174l1700185a138"]
    name = "kijiji_car_suv_spider"


class KijijiCarVanSpider(KijijiCarSpider):
    name = "kijiji_car_van_spider"
    start_urls = ["http://www.kijiji.ca/b-cars-trucks/ottawa/mini+van/c174l1700185a138"]
    name = "kijiji_car_van_spider"
