# -*- coding: utf-8 -*-

from parameterized import parameterized

from app.api.helpers.data_layers import MOVE_TYPE_ARCHIVED
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse


class TestMoveCreateArchive(BaseTestCase):
    """Test Move create Archive"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateArchive, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
    ])
    @request_context
    def test_move_create_archive_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)
        assert self.send_post(payload, user=user, code=403)

    @parameterized.expand([
        ['user_1'],
        ['admin'],
    ])
    @request_context
    def test_move_create_archive_as_owner(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret(owner=self.user_1)
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)
        assert self.send_post(payload, user=user, code=201)
