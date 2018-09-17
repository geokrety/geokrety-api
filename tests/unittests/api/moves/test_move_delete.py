# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.move import MoveResponse


class TestGeokretyDelete(BaseTestCase):
    """Test Geokrety delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves/%s?%s" % (obj_id, args_)
        return MoveResponse(self._send_delete(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],  # author
        ['user_1', 200],  # author
        ['user_2', 403],
    ])
    @request_context
    def test_moves_delete_is_forbidden_as(self, username, expected):
        moves = self.blend_move(author=self.user_1)
        user = getattr(self, username) if username else None
        assert self.send_delete(moves.id, user=user, code=expected)
