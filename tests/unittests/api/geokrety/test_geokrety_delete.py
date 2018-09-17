# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.geokret import GeokretResponse


class TestGeokretyDelete(BaseTestCase):
    """Test Geokrety delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety/%s?%s" % (obj_id, args_)
        return GeokretResponse(self._send_delete(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_geokrety_delete_is_forbidden_as(self, username, expected):
        geokrety = self.blend_geokret()
        user = getattr(self, username) if username else None
        assert self.send_delete(geokrety.id, user=user, code=expected)

    @request_context
    def test_geokrety_delete_is_allowed_as_admin(self):
        geokrety = self.blend_geokret()
        assert self.send_delete(geokrety.id, user=self.admin)
