# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  request_context)
from tests.unittests.utils.responses.moves_types import MovesTypesResponse


class fakeMovesType(object):
    def __init__(self, name):
        self.name = name


class TestMovesTypeDetails(BaseTestCase):
    """Test Moves Types details"""

    def send_get(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves-types/%s?%s" % (obj_id, args_)
        return MovesTypesResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, 'Dropped to'],
        [MOVE_TYPE_GRABBED, 'Grabbed from'],
        [MOVE_TYPE_COMMENT, 'A comment'],
        [MOVE_TYPE_SEEN, 'Seen in'],
        [MOVE_TYPE_ARCHIVED, 'Archived'],
        [MOVE_TYPE_DIPPED, 'Dipped'],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_moves_types_details_has_normal_attributes_as_anonymous_user(self, move_type, expected):
        fake_type = fakeMovesType(expected)
        response = self.send_get(move_type)
        response.assertHasAttribute('name', fake_type.name)
        response.assertHasPublicAttributes(fake_type)
