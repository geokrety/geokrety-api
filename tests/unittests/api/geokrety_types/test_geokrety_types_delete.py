# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  request_context)
from tests.unittests.utils.responses.geokrety_types import \
    GeokretyTypesResponse


class TestGeokretyTypeDelete(BaseTestCase):
    """Test GeoKrety Types delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety-types/%s?%s" % (obj_id, args_)
        return GeokretyTypesResponse(self._send_patch(url, **kwargs).get_json())

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],
        ['user_2'],
    ])
    @request_context
    def test_geokrety_types_delete_objects_are_immuable(self, username):
        user = getattr(self, username) if username else None
        self.send_delete(1, user=user, code=405)
