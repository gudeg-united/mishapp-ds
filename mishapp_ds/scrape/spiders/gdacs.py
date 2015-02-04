# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta

import scrapy

from mishapp_ds.scrape.items import GdacsItem
from mishapp_ds.scrape.loaders import GdacsItemLoader

GDACS_URL_FMT = (
    "http://www.gdacs.org/transform.aspx"
    "?xmlurl=http://www.gdacs.org/rss.aspx%3Fprofile%3DARCHIVE"
    "%26from%3D{start}%26to%3D{end}%26alertlevel%3D"
    "%26country%3D{country}%26eventtype%3D{event_type}"
    "&xslurl=http://www.gdacs.org/xslt/gdacs_table.xslt"
    "&pname=|eventtypes&pvalue=|{event_type}"
    )


class GdacsSpider(scrapy.Spider):
    name = "gdacs"
    allowed_domains = ["gdacs.org"]

    def __init__(self, country="Indonesia", event_type="EQ"):
        now = datetime.utcnow()
        today = now.strftime("%Y-%m-%d")
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

        self.start_urls = [
            GDACS_URL_FMT.format(country=country, event_type=event_type,
                                 start=yesterday, end=today),
        ]

    def parse(self, response):
        for tr in iter(response.css("tr")[2:]):
            cols = tr.css("td")

            loader = GdacsItemLoader(GdacsItem())
            loader.add_value("source", self.name)
            loader.add_value("source_id", cols[0].css("a::text").extract())
            loader.add_value("country", cols[2].css("::text").extract())
            loader.add_value(
                "magnitude", cols[3].css("::text").re("Magnitude (.+)M"))
            loader.add_value("date_time", cols[4].css("span::text").extract())
            loader.add_value(
                "depth", cols[3].css("::text").re("Depth:(.+)km"))
            loader.add_value("impact", cols[5].css("::text").extract())
            loader.add_value("lat", cols[6].css("::text").re("(.+),"))
            loader.add_value(
                "lon", cols[6].css("::text").re(r",[\r|\n|\t|\s]+(.+)"))
            yield loader.load_item()
