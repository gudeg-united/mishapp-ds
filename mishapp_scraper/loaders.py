from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import arrow
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join
from scrapy.contrib.loader.processor import MapCompose


def wib_to_utc(value):
    value = value.replace("WIB", "+07:00")
    local = arrow.get(value, "DD-MM-YYYY HH:mm:ss Z")
    utc = local.to("UTC")
    return str(utc)


class BmkgItemLoader(ItemLoader):
    default_output_processor = Join()
    date_time_in = MapCompose(wib_to_utc)
