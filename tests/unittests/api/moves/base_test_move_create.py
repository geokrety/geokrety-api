# -*- coding: utf-8 -*-

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.static_test_cases import EMPTY_TEST_CASES


class _BaseTestMoveCreate(BaseTestCase):
    """Base tests with optional coordinates"""

    move_type = None

    def setUp(self):
        assert self.move_type is not None
        super(_BaseTestMoveCreate, self).setUp()

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(_BaseTestMoveCreate, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        [u'ééééé'],
        [u'<'],
        [u'\x01 '],
        [u'";!'],
    ])
    @request_context
    def test_field_tracking_code_must_be_alphanumeric(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @request_context
    def test_field_tracking_code_must_be_present(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        del payload['data']['attributes']['tracking-code']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_field_tracking_code_cannot_be_blank(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')
