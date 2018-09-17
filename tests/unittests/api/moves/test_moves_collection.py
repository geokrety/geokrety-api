# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  request_context)
from tests.unittests.utils.responses.collections import MovesCollectionResponse


class TestMoveCollection(BaseTestCase):
    """Test Move details"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves?%s" % (args_)
        return MovesCollectionResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],  # Owner
        ['user_2'],
    ])
    @request_context
    def test_move_collection_has_normal_attributes_as(self, username):
        user = getattr(self, username) if username else None
        moves = self.blend_move(author=self.user_1, count=3)
        response = self.send_get(user=user)
        i = 0
        for response_ in response.data:
            response_.assertHasPublicAttributes(moves[i])
            i = i + 1

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_collection_has_coordinates_as(self, move_type):
        moves = self.blend_move(type=move_type, author=self.user_1, count=3)
        response = self.send_get()
        i = 0
        for response_ in response.data:
            response_.assertHasPublicAttributes(moves[i])
            response_.assertHasAttribute('latitude', moves[i].latitude)
            response_.assertHasAttribute('longitude', moves[i].longitude)
            i = i + 1

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_ARCHIVED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_collection_dont_have_coordinates_as(self, move_type):
        moves = self.blend_move(type=move_type, author=self.user_1, count=3)
        response = self.send_get()
        i = 0
        for response_ in response.data:
            response_.assertHasPublicAttributes(moves[i])
            response_.assertHasAttribute('latitude', None)
            response_.assertHasAttribute('longitude', None)
            i = i + 1
