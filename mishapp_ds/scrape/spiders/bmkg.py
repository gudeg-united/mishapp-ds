# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

import scrapy

from mishapp_ds.scrape.items import BmkgItem
from mishapp_ds.scrape.loaders import BmkgEarthquakeItemLoader
from mishapp_ds.scrape.loaders import BmkgTsunamiItemLoader

# URL to BMKG page where earthquake data reside
BMKG_EARTHQUAKE_URL = "http://bmkg.go.id/BMKG_Pusat" \
                      "/Gempabumi_-_Tsunami/Gempabumi/Gempabumi_Dirasakan.bmkg"

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
            # Common data are extracted using `.//td/text()`,
            # but date value is located under `td > a`,
            # hence we're adding `|.//td/a/text()` in xpath expression
            # to correctly extract date as well.
            #
            # For example::
            #
            #    <tr>
            #        <td>118</td>
            #        <td><a href="#">2000-01-02</a></td>
            #    </tr>
            cols = tr.xpath(".//td/text()|.//td/a/text()").extract()[1:6]
            lat, lon = earthquake_latlon(cols[2])

            loader = BmkgEarthquakeItemLoader(BmkgItem())
            loader.add_value("date_time", " ".join(cols[:2]))
            loader.add_value("lat", lat)
            loader.add_value("lon", lon)
            loader.add_value("magnitudo", cols[3])
            loader.add_value("depth", cols[4])
            loader.add_value("type", "earthquake")
            yield loader.load_item()

    def parse_tsunami(self, response):
        for tr in iter(response.css("tbody tr")):
            cols = tr.css("td::text").extract()
            lat, lon = cols[2].split(" - ")

            loader = BmkgTsunamiItemLoader(BmkgItem())
            loader.add_value("date_time", " ".join(cols[:2]))
            loader.add_value("lat", lat)
            loader.add_value("lon", lon)
            loader.add_value("magnitudo", cols[3])
            loader.add_value("depth", cols[4])
            loader.add_value("type", "tsunami")
            yield loader.load_item()


# lat lon regex format for earthquake datasource
eq_latlon_re = re.compile(r"(?P<lat>.+) L[U|S] (?P<lon>.+) B[B|T]")


def earthquake_latlon(value):
    """Gets latitude and longitude from a string.

    :param value: Latlon string, for example `3.24 LS 128.96 BT`.
    :returns: A tuple of lat and lon strings.
    """
    lat, lon = "", ""
    rgx = eq_latlon_re.match(value)

    if rgx:
        lat, lon = rgx.groups()
    return lat, lon
