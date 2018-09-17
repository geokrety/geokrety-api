# -*- coding: utf-8 -*-

import urllib

from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  request_context)
from tests.unittests.utils.responses.collections import \
    GeokretyTypesCollectionResponse


class TestGeokretyTypeCollection(BaseTestCase):
    """Test GeoKrety Types collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety-types?%s" % (args_)
        return GeokretyTypesCollectionResponse(self._send_get(url, **kwargs).get_json())

    @request_context
    def test_geokrety_types_collection_has_right_number_of_items(self):
        response = self.send_get()
        self.assertEqual(response.count, 5)
