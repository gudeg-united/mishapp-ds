from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize("value, format_, expectation", [
    ("01-Jan-15 10:00:00 WIB", "DD-MMM-YY HH:mm:ss Z", "2015-01-01T03:00:00+00:00"),  # noqa
    ("01/01/2015 10:00:00 WIB", "DD/MM/YYYY HH:mm:ss Z", "2015-01-01T03:00:00+00:00"),  # noqa
])
def test_wib_to_utc(value, format_, expectation):
    from mishapp_ds.scrape.loaders import wib_to_utc
    assert wib_to_utc(value, format_) == expectation
