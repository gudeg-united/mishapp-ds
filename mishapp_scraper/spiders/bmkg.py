# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy
from mishapp_scraper.items import BmkgItem
from mishapp_scraper.loaders import BmkgItemLoader


class BmkgSpider(scrapy.Spider):
    name = "bmkg"
    allowed_domains = ["bmkg.go.id"]
    start_urls = (
        "http://bmkg.go.id/BMKG_Pusat/Gempabumi_-_Tsunami/Gempabumi/Gempabumi_Terkini.bmkg",  # noqa
        )

    def parse(self, response):
        for tr in iter(response.css("tbody tr")):
            # first column is omitted
            cols = tr.css("td::text").extract()[1:]
            loader = BmkgItemLoader(BmkgItem(), selector=None)
            loader.add_value("date_time", cols[0])
            loader.add_value("lat", cols[1])
            loader.add_value("lon", cols[2])
            loader.add_value("magnitudo", cols[3])
            loader.add_value("depth", cols[4])
            yield loader.load_item()
