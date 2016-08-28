import scrapy
import re

from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from BaseSpider import BaseSpider

class NrcanFuelRatingsSpider(BaseSpider):
    name = "nrcan_fuel_ratings_spider"
    allowed_domains = [
        "http://oee.nrcan.gc.ca"
    ]
    start_urls = [
        "http://oee.nrcan.gc.ca/fcr-rcf/public/index-e.cfm?submitted=true&sort=overall_rank&searchbox=&year=2016&class=all&make=all&model=all&trans=all&FT=all&cylinders=all&unit=0&kmPerYear=&cityRating=&fuelGas=&fuelPremium=&fuelDiesel=&onSearchLink=%231&pageSize=100&btnSearch=Search#aSearch"
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "http://oee.nrcan.gc.ca/fcr-rcf/public/report-e.cfm\?.*reportID=.*"
                ]
            ),
            callback='parse_item'
        ),
        Rule(

            LinkExtractor(
                allow=["http://oee.nrcan.gc.ca/fcr-rcf/public/index-e.cfm.*start=[0-9][0-9]*.*"]
            )
        )
    ]

    def parse_item(self, response):
        item = items.FuelRatingItem()

        item["url"] = response.url
        item["domain"] = self._extract_domain(response)

        title = self._extract_text_from_class(response, "h2", "title")
        item["title"] = title

        l = title.split(" ")
        item["make"] = l[0]
        item["model"] = " ".join(l[1:])

        item["year"] = self._extract_field(response, "Model Year")
        item["lphkm_city"] = self._extract_field(response, "City")
        item["lphkm_hwy"] = self._extract_field(response, "Highway")
        item["estimated_fuel_cost_year"] = self._extract_field(response, "Annual Fuel Cost")

        return item

    def _extract_field(self, response, fieldname):
        l = response.xpath("//th[contains(text(), '{0}')]/following::td[1]//./text()".
                format(fieldname)).extract()
        return l[0].strip() if l else None

