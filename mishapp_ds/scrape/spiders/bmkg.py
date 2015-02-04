# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from hashlib import md5
# import re

import scrapy

from mishapp_ds.scrape.items import BmkgItem
from mishapp_ds.scrape.loaders import BmkgEarthquakeItemLoader
from mishapp_ds.scrape.loaders import BmkgTsunamiItemLoader

# URL to BMKG page where latest earthquake data reside
BMKG_EARTHQUAKE_URL = \
    "http://bmkg.go.id/BMKG_Pusat" \
    "/Gempabumi_-_Tsunami/Gempabumi/Gempabumi_Terkini.bmkg"

# URL to BMKG page where tsunami data reside
BMKG_TSUNAMI_URL = "http://bmkg.go.id/BMKG_Pusat" \
                   "/Gempabumi_-_Tsunami/Tsunami.bmkg"


class BmkgSpider(scrapy.Spider):
    name = "bmkg"
    allowed_domains = ["bmkg.go.id"]
    start_urls = [BMKG_TSUNAMI_URL, BMKG_EARTHQUAKE_URL]

    def parse(self, response):
        parser_map = {
            BMKG_EARTHQUAKE_URL: self.parse_earthquake,
            BMKG_TSUNAMI_URL: self.parse_tsunami,
        }
        callback = parser_map.get(response.url)
        if callback:
            return callback(response)

    def parse_earthquake(self, response):
        for tr in iter(response.css("tbody tr")):
            cols = tr.xpath(".//td/text()|.//td/a/text()").extract()[1:6]

            loader = BmkgEarthquakeItemLoader(BmkgItem())
            loader.add_value("date_time", cols[0])
            loader.add_value("lat", cols[1])
            loader.add_value("lon", cols[2])
            loader.add_value("magnitude", cols[3])
            loader.add_value("depth", cols[4], re="(.+) Km")
            loader.add_value("disaster_type", "earthquake")
            loader.add_value("source", self.name)
            loader.add_value("source_id", generate_source_id(loader))
            yield loader.load_item()

    def parse_tsunami(self, response):
        for tr in iter(response.css("tbody tr")):
            cols = tr.css("td::text").extract()
            lat, lon = cols[2].split(" - ")

            loader = BmkgTsunamiItemLoader(BmkgItem())
            loader.add_value("date_time", " ".join(cols[:2]))
            loader.add_value("lat", lat)
            loader.add_value("lon", lon)
            loader.add_value("magnitude", cols[3], re="(.+) SR")
            loader.add_value("depth", cols[4], re="(.+) Km")
            loader.add_value("disaster_type", "tsunami")
            loader.add_value("source", self.name)
            loader.add_value("source_id", generate_source_id(loader))
            yield loader.load_item()


def generate_source_id(loader):
    """Generates md5 hash from required item keys.
    """
    keys = ["date_time", "lat", "lon", "disaster_type"]
    values = [loader.get_output_value(key) for key in keys]

    assert all(values), "All required values are not loaded properly."
    return md5("-".join(values)).hexdigest()
