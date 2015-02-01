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
