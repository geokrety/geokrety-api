# -*- coding: utf-8 -*-

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED,
                                         MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_double_move_type,
                                                  request_context)
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse


class TestHolder(BaseTestCase):
    """Test Holder"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestHolder, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        [MOVE_TYPE_GRABBED, MOVE_TYPE_GRABBED, 'user_1', 'user_2'],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_DROPPED, 'user_1', None],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_COMMENT, 'user_1', 'user_1'],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN, 'user_1', None],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_DIPPED, 'user_1', 'user_2'],

        [MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED, None, 'user_2'],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_DROPPED, None, None],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_COMMENT, None, None],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN, None, None],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_DIPPED, None, 'user_2'],

        [MOVE_TYPE_COMMENT, MOVE_TYPE_GRABBED, None, 'user_2'],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_DROPPED, None, None],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_COMMENT, None, None],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_SEEN, None, None],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED, None, 'user_2'],

        [MOVE_TYPE_SEEN, MOVE_TYPE_GRABBED, None, 'user_2'],
        [MOVE_TYPE_SEEN, MOVE_TYPE_DROPPED, None, None],
        [MOVE_TYPE_SEEN, MOVE_TYPE_COMMENT, None, None],
        [MOVE_TYPE_SEEN, MOVE_TYPE_SEEN, None, None],
        [MOVE_TYPE_SEEN, MOVE_TYPE_DIPPED, None, 'user_2'],

        [MOVE_TYPE_DIPPED, MOVE_TYPE_GRABBED, 'user_1', 'user_2'],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED, 'user_1', None],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_COMMENT, 'user_1', 'user_1'],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_SEEN, 'user_1', None],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_DIPPED, 'user_1', 'user_2'],
    ], doc_func=custom_name_geokrety_double_move_type)
    @request_context
    def test_holder_must_be_updated(self, move_type1, move_type2, username1, username2):
        user_id1 = getattr(self, username1).id if username1 else None
        user_id2 = getattr(self, username2).id if username2 else None

        geokret = self.blend_geokret(created_on_datetime="2018-10-11T20:13:35")
        self.blend_move(type=move_type1, author=self.user_1,
                        geokret=geokret, moved_on_datetime="2018-10-11T21:49:55")

        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret, moved_on_datetime="2018-10-11T23:10:53")
        self.send_post(payload, user=self.user_2, code=201)
        self.assertEqual(geokret.holder_id, user_id1)

        payload = MovePayload(move_type2, geokret=geokret, moved_on_datetime="2018-10-11T23:10:55")\
            .set_coordinates()
        self.send_post(payload, user=self.user_2, code=201)
        self.assertEqual(geokret.holder_id, user_id2)
