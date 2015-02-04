# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy


class _DisasterItem(scrapy.Item):
    # lowercased source name, e.g. bmkg
    source = scrapy.Field()

    # unique data item ID
    source_id = scrapy.Field()

    # disaster type, e.g. earthquake
    disaster_type = scrapy.Field()

    # when was the disaster occur
    date_time = scrapy.Field()

    # latitude
    lat = scrapy.Field()

    # longitude
    lon = scrapy.Field()

    country = scrapy.Field()


class BmkgItem(_DisasterItem):
    """This class represents desired data from BMKG.

    Things to be aware of:

    * latitude is called `lintang`
    * longitude is called `bujur`
    """

    # magnitude in SR
    magnitude = scrapy.Field()

    # depth in Km
    depth = scrapy.Field()


class GdacsItem(_DisasterItem):
    # magnitude in M
    magnitude = scrapy.Field()

    # depth in Km
    depth = scrapy.Field()

    impact = scrapy.Field()
