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


class TestLastMove(BaseTestCase):
    """Test Last Move"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestLastMove, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        [MOVE_TYPE_GRABBED, MOVE_TYPE_GRABBED],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_COMMENT],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN],
        [MOVE_TYPE_GRABBED, MOVE_TYPE_DIPPED],

        [MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_DROPPED],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_COMMENT],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN],
        [MOVE_TYPE_DROPPED, MOVE_TYPE_DIPPED],

        [MOVE_TYPE_COMMENT, MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_DROPPED],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_COMMENT],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_SEEN],
        [MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED],

        [MOVE_TYPE_SEEN, MOVE_TYPE_GRABBED],
        [MOVE_TYPE_SEEN, MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN, MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN, MOVE_TYPE_SEEN],
        [MOVE_TYPE_SEEN, MOVE_TYPE_DIPPED],

        [MOVE_TYPE_DIPPED, MOVE_TYPE_GRABBED],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_COMMENT],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED, MOVE_TYPE_DIPPED],

        [None, MOVE_TYPE_GRABBED],
        [None, MOVE_TYPE_DROPPED],
        [None, MOVE_TYPE_COMMENT],
        [None, MOVE_TYPE_SEEN],
        [None, MOVE_TYPE_DIPPED],

        [None, None, False],
    ], doc_func=custom_name_geokrety_double_move_type)
    @request_context
    def test_last_move_must_be_updated(self, move_type1, move_type2, result_move2=True):
        geokret = self.blend_geokret(created_on_datetime="2018-12-24T15:35:45")
        if move_type1 is not None:
            self.blend_move(type=move_type1, author=self.user_1,
                            geokret=geokret, moved_on_datetime="2018-12-24T15:38:11")
        if move_type2 is not None:
            payload = MovePayload(move_type2, geokret=geokret, moved_on_datetime="2018-12-24T15:51:12")\
                .set_coordinates()
            move2 = self.send_post(payload, user=self.user_1, code=201)

        last_move = move2.id if result_move2 else None
        self.assertEqual(geokret.last_move_id, last_move)
