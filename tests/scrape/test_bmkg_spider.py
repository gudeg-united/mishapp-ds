from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def test_generate_source_id():
    from mishapp_ds.scrape.spiders.bmkg import generate_source_id
    from mishapp_ds.scrape.loaders import BmkgEarthquakeItemLoader
    from mishapp_ds.scrape.items import BmkgItem

    loader = BmkgEarthquakeItemLoader(BmkgItem())
    loader.add_value("date_time", "01-01-2015 10:00:00 WIB")
    loader.add_value("lat", "0.12")
    loader.add_value("lon", "123.85")
    loader.add_value("disaster_type", "earthquake")
    assert generate_source_id(loader)
