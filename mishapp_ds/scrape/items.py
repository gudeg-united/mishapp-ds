# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy


class BmkgItem(scrapy.Item):
    date_time = scrapy.Field()

    # `lintang`
    lat = scrapy.Field()

    # `bujur`
    lon = scrapy.Field()

    magnitude = scrapy.Field()

    depth = scrapy.Field()

    type = scrapy.Field()
