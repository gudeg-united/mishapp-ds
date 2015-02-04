from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize("value, expectation", [
    ("123 LS 123 BT", ("123", "123")),
    ("123 LU 123 BT", ("123", "123")),
    ("123 LS 123 BB", ("123", "123")),
    ("123 LU 123 BB", ("123", "123")),
])
def test_earthquake_latlon(value, expectation):
    from mishapp_ds.scrape.spiders.bmkg import earthquake_latlon
    assert earthquake_latlon(value) == expectation


def test_generate_source_id():
    from mishapp_ds.scrape.spiders.bmkg import generate_source_id
    from mishapp_ds.scrape.loaders import BmkgEarthquakeItemLoader
    from mishapp_ds.scrape.items import BmkgItem

    loader = BmkgEarthquakeItemLoader(BmkgItem())
    loader.add_value("date_time", "01/01/2015 10:00:00 WIB")
    loader.add_value("lat", "0.12")
    loader.add_value("lon", "123.85")
    loader.add_value("disaster_type", "earthquake")
    assert generate_source_id(loader)
