# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  request_context)
from tests.unittests.utils.responses.move import MoveResponse


class TestMoveDetails(BaseTestCase):
    """Test Move details"""

    def send_get(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves/%s?%s" % (obj_id, args_)
        return MoveResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],  # Owner
        ['user_2'],
    ])
    @request_context
    def test_move_details_has_public_attributes_as(self, username):
        user = getattr(self, username) if username else None
        move = self.blend_move()
        response = self.send_get(move.id, user=user)
        response.assertHasPublicAttributes(move)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
        [MOVE_TYPE_GRABBED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_details_has_coordinates_as(self, move_type):
        move = self.blend_move(type=move_type)
        response = self.send_get(move.id)
        response.assertHasPublicAttributes(move)
        response.assertHasAttribute('latitude', move.latitude)
        response.assertHasAttribute('longitude', move.longitude)

    @parameterized.expand([
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_ARCHIVED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_details_dont_have_coordinates_as(self, move_type):
        move = self.blend_move(type=move_type)
        response = self.send_get(move.id)
        response.assertHasPublicAttributes(move)
        with self.assertRaises(AssertionError):
            response.assertHasAttribute('latitude', move.latitude)
        with self.assertRaises(AssertionError):
            response.assertHasAttribute('longitude', move.longitude)
