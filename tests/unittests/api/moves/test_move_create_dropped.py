# -*- coding: utf-8 -*-

from parameterized import parameterized

from app.api.helpers.data_layers import MOVE_TYPE_DROPPED
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.static_test_cases import EMPTY_TEST_CASES


class TestMoveCreateDropped(BaseTestCase):
    """Test Move create Dropped"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateDropped, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_move_create_dropped_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret)\
            .set_coordinates()
        assert self.send_post(payload, user=user)

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_move_create_dropped_field_waypoint_can_be_absent(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('waypoint', None)
        response = self.send_post(payload, user=user, code=201)
        response.assertHasAttribute('waypoint', '')

    @parameterized.expand([
        [None],
        [u''],
    ])
    @request_context
    def test_move_create_dropped_field_waypoint_can_be_empty(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')
