# -*- coding: utf-8 -*-

from parameterized import parameterized

from app.api.helpers.data_layers import MOVE_TYPE_GRABBED
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.static_test_cases import EMPTY_TEST_CASES


class TestMoveCreateGrabbed(BaseTestCase):
    """Test Move create Grabbed"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateGrabbed, self)._send_post(
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
    def test_move_create_grabbed_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        assert self.send_post(payload, user=user)

    @request_context
    def test_move_create_grabbed_field_tracking_code_must_be_present(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        del payload['data']['attributes']['tracking-code']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_move_create_grabbed_field_tracking_code_cannot_be_blank(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @request_context
    def test_move_create_grabbed_field_altitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('altitude', -32768)

    @request_context
    def test_move_create_grabbed_field_country_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('country', '')

    @request_context
    def test_move_create_grabbed_field_distance_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('distance', 0)

    @request_context
    def test_move_create_grabbed_field_waypoint_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @request_context
    def test_move_create_grabbed_field_latitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)

    @request_context
    def test_move_create_grabbed_field_longitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('longitude', None)