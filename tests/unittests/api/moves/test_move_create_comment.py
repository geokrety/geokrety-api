# -*- coding: utf-8 -*-

from parameterized import parameterized

from app.api.helpers.data_layers import MOVE_TYPE_COMMENT
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse


class TestMoveCreateComment(BaseTestCase):
    """Test Move create comment"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateComment, self)._send_post(
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
        [u'ABC123'],
    ])
    @request_context
    def test_field_tracking_code_must_be_alphanumeric(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret)\
            .set_coordinates()
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @request_context
    def test_field_tracking_code_must_be_present_if_id_not_given(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret)
        payload['data']['attributes'].pop('tracking-code', None)
        payload['data']['attributes'].pop('id', None)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @request_context
    def test_field_tracking_code_may_be_ommited_if_id_was_given(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret)
        payload.set_geokret_id(geokret.id)
        payload['data']['attributes'].pop('tracking-code', None)
        response = self.send_post(payload, user=self.user_1)
        response.assertHasRelationshipGeokretData(geokret.id)

    @request_context
    def test_field_id_may_be_ommited_if_tracking_code_was_given(self):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret)
        payload.set_tracking_code(geokret.tracking_code)
        response = self.send_post(payload, user=self.user_1)
        response.assertHasRelationshipGeokretData(geokret.id)
