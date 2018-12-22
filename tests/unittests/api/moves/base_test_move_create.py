# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase
from tests.unittests.utils.responses.move import MoveResponse


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
