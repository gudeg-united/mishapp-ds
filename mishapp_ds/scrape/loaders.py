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
from scrapylib.processors import strip


def datetime_to_utc(value, format_):
    local = arrow.get(value, format_)
    utc = local.to("UTC")
    return str(utc)


class BmkgItemLoaderBase(ItemLoader):
    default_output_processor = Join()


class BmkgTsunamiItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        lambda v: v.strip().replace("WIB", "+07:00"),
        partial(datetime_to_utc, format_="DD-MMM-YY HH:mm:ss Z"),
        )


class BmkgEarthquakeItemLoader(BmkgItemLoaderBase):
    date_time_in = MapCompose(
        lambda v: v.strip().replace("WIB", "+07:00"),
        partial(datetime_to_utc, format_="DD-MM-YYYY HH:mm:ss Z"),
        )


class GdacsItemLoaderBase(ItemLoader):
    default_output_processor = Join()


class GdacsEarthquakeItemLoader(GdacsItemLoaderBase):
    date_time_in = MapCompose(
        clean_spaces,
        lambda v: v.strip().replace("UTC", ""),
        )

    date_time_out = Compose(
        lambda v: " ".join(v),
        partial(datetime_to_utc, format_="DD MMM YYYY HH:mm"),
        )


class GdacsFloodItemLoader(GdacsItemLoaderBase):
    date_time_out = Compose(
        lambda v: " ".join(v),
        partial(datetime_to_utc, format_="DD MMM YYYY"),
        )

    date_time_end_out = date_time_out


class GdacsCycloneItemLoader(GdacsItemLoaderBase):
    country_in = MapCompose(clean_spaces, strip)
