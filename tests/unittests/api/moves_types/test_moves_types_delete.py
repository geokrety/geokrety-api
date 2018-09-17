# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  request_context)
from tests.unittests.utils.responses.moves_types import \
    MovesTypesResponse


class TestMovesTypeDelete(BaseTestCase):
    """Test Moves Types delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves-types/%s?%s" % (obj_id, args_)
        return MovesTypesResponse(self._send_patch(url, **kwargs).get_json())

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],
        ['user_2'],
    ])
    @request_context
    def test_moves_types_delete_objects_are_immuable(self, username):
        user = getattr(self, username) if username else None
        self.send_delete(1, user=user, code=405)
