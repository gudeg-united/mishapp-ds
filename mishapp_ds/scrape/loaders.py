from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from functools import partial

import arrow
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join
from scrapy.contrib.loader.processor import MapCompose


def wib_to_utc(value, format_):
    value = value.replace("WIB", "+07:00")
    local = arrow.get(value, format_)
    utc = local.to("UTC")
    return str(utc)


class BmkgItemLoaderBase(ItemLoader):
    default_output_processor = Join()


class BmkgTsunamiItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        partial(wib_to_utc, format_="DD-MMM-YY HH:mm:ss Z"),
        )


class BmkgEarthquakeItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        partial(wib_to_utc, format_="DD/MM/YYYY HH:mm:ss Z"),
        )