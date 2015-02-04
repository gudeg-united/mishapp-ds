from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from functools import partial

import arrow
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import Compose
from scrapylib.processors import clean_spaces


def datetime_to_utc(value, format_):
    value = value.replace("WIB", "+07:00")
    local = arrow.get(value, format_)
    utc = local.to("UTC")
    return str(utc)


# backward-compat
wib_to_utc = datetime_to_utc


class BmkgItemLoaderBase(ItemLoader):
    default_output_processor = Join()


class BmkgTsunamiItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        partial(wib_to_utc, format_="DD-MMM-YY HH:mm:ss Z"),
        )


class BmkgEarthquakeItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        partial(wib_to_utc, format_="DD-MM-YYYY HH:mm:ss Z"),
        )


class GdacsItemLoader(ItemLoader):
    default_output_processor = Join()

    date_time_in = MapCompose(
        clean_spaces,
        lambda v: v.strip().replace("UTC", ""),
        )

    date_time_out = Compose(
        lambda v: " ".join(v),
        partial(datetime_to_utc, format_="DD MMM YYYY HH:mm"),
        )
