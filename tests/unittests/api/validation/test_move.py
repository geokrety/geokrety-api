# coding=utf-8
from app import current_app as app
from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.schema.moves import MoveSchema
from app.models.geokret import Geokret
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestMove(GeokretyTestCase):
    """Test Move Schema"""

    def test_validate_(self):
        """Check Form Move: validates move_type_id"""
        with app.test_request_context():
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_GRABBED)

    def test_validate_move_type_id(self):
        """Check Form Move: validates move_type_id"""
        with app.test_request_context():
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_GRABBED)
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_COMMENT)
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_DROPPED)
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_SEEN)
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_ARCHIVED)
            MoveSchema.validate_move_type_id_valid(MoveSchema(), MOVE_TYPE_DIPPED)

            with self.assertRaises(UnprocessableEntity):
                MoveSchema.validate_move_type_id_valid(MoveSchema(), -1)
                MoveSchema.validate_move_type_id_valid(MoveSchema(), 1)
                MoveSchema.validate_move_type_id_valid(MoveSchema(), 6)
                MoveSchema.validate_move_type_id_valid(MoveSchema(), "-1")
                MoveSchema.validate_move_type_id_valid(MoveSchema(), "6")
                MoveSchema.validate_move_type_id_valid(MoveSchema(), "")
                MoveSchema.validate_move_type_id_valid(MoveSchema(), "100")
                MoveSchema.validate_move_type_id_valid(MoveSchema(), "A")
                MoveSchema.validate_move_type_id_valid(MoveSchema(), u"jeśli")

    def test_validate_tracking_code_is_valid(self):
        """Check Form Move: validates tracking_code"""
        with app.test_request_context():
            mixer.init_app(app)
            geokret1 = mixer.blend(Geokret)

            MoveSchema.validate_tracking_code_is_valid(MoveSchema(), geokret1.tracking_code)

            with self.assertRaises(UnprocessableEntity):
                self.assertNotEqual(geokret1.tracking_code, "AAAAA")
                MoveSchema.validate_tracking_code_is_valid(MoveSchema(), "AAAAA")
                MoveSchema.validate_tracking_code_is_valid(MoveSchema(), "")
                MoveSchema.validate_tracking_code_is_valid(MoveSchema(), u"jeśli")
                MoveSchema.validate_tracking_code_is_valid(MoveSchema(), "1234567890")
