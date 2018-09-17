# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.user import UserResponse


class TestUsersDelete(BaseTestCase):
    """Test Users delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/users/%s?%s" % (obj_id, args_)
        return UserResponse(self._send_delete(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_users_delete_as(self, username, expected):
        user = getattr(self, username) if username else None
        assert self.send_delete(self.user_1.id, user=user, code=expected)
