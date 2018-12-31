from mixer.backend.flask import mixer

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED,
                                         MOVE_TYPE_SEEN)
from app.api.helpers.move_tasks import (update_geokret_holder,
                                        update_geokret_total_moves_count,
                                        update_move_country_and_altitude,
                                        update_move_distances)
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.user import User
from tests.unittests.utils.base_test_case import BaseTestCase, request_context


class TestMoveTasksHelper(BaseTestCase):

    def _blend(self):
        """Create mocked Geokret/User"""
        mixer.init_app(app)
        with mixer.ctx():
            # Users
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            self.user3 = mixer.blend(User)
            self.user4 = mixer.blend(User)

            self.geokret1 = mixer.blend(Geokret, type=GEOKRET_TYPE_TRADITIONAL,
                                        owner=self.user1, holder=self.user1, tracking_code="ABC123",
                                        created_on_datetime="2017-12-01T14:18:22")

            # Moves
            self.move1 = mixer.blend(Move, type=MOVE_TYPE_DROPPED, geokret=self.geokret1,
                                     author=self.user2, moved_on_datetime="2017-12-01T14:21:22",
                                     latitude=43.694483, longitude=6.85575)
            self.move2 = mixer.blend(Move, type=MOVE_TYPE_COMMENT, geokret=self.geokret1,
                                     author=self.user1, moved_on_datetime="2017-12-01T14:24:22")
            self.move3 = mixer.blend(Move, type=MOVE_TYPE_DIPPED, geokret=self.geokret1,
                                     author=self.user4, moved_on_datetime="2017-12-01T14:25:22",
                                     latitude=43.704233, longitude=6.869833)
            self.move4 = mixer.blend(Move, type=MOVE_TYPE_DIPPED, geokret=self.geokret1,
                                     author=self.user4, moved_on_datetime="2017-12-01T14:23:22",
                                     latitude=43.6792, longitude=6.852933)
            self.move5 = mixer.blend(Move, type=MOVE_TYPE_SEEN, geokret=self.geokret1,
                                     author=self.user3, moved_on_datetime="2017-12-01T14:22:22",
                                     latitude=43.701767, longitude=6.84085)
            self.move6 = mixer.blend(Move, type=MOVE_TYPE_GRABBED, geokret=self.geokret1,
                                     author=self.user2, moved_on_datetime="2017-12-01T14:19:22")
            self.move7 = mixer.blend(Move, type=MOVE_TYPE_COMMENT, geokret=self.geokret1,
                                     author=self.user2, moved_on_datetime="2017-12-01T14:20:22")
            self.move8 = mixer.blend(Move, type=MOVE_TYPE_DROPPED, geokret=self.geokret1,
                                     author=self.user1, moved_on_datetime="2017-12-01T14:18:22",
                                     latitude=43.693633, longitude=6.860933)
            self.move9 = mixer.blend(Move, type=MOVE_TYPE_COMMENT, geokret=self.geokret1,
                                     author=self.user3, moved_on_datetime="2017-12-01T14:28:22")

    def test_update_move_distances(self):
        """Check Move Tasks: compute move distances"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_distances(self.geokret1.id)
            db.session.commit()

            # Check in database
            moves = Move.query.filter(Move.geokret_id == self.geokret1.id) \
                .order_by(Move.moved_on_datetime.asc()).all()
            self.assertEqual(moves[0].distance, 0)
            self.assertEqual(moves[1].distance, 0)
            self.assertEqual(moves[2].distance, 0)
            self.assertEqual(moves[3].distance, int(round(0.428142805874)))
            self.assertEqual(moves[4].distance, int(round(1.44869620611)))
            self.assertEqual(moves[5].distance, int(round(2.69014884056)))
            self.assertEqual(moves[6].distance, 0)
            self.assertEqual(moves[7].distance, int(round(3.09681445874)))

    def test_update_geokret_total_distance(self):
        """Check Move Tasks: compute GeoKret total distance"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_distances(self.geokret1.id)
            db.session.commit()

            # Check in database
            self.assertEqual(self.geokret1.distance, 7)

    def test_update_geokret_caches_count(self):
        """Check Move Tasks: compute GeoKret total caches count"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_geokret_total_moves_count(self.geokret1.id)
            db.session.commit()

            # Check in database
            self.assertEqual(self.geokret1.caches_count, 5)

    def test_update_geokret_holder(self):
        """Check Move Tasks: compute GeoKret holder"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_geokret_holder(self.geokret1.id)
            db.session.commit()

            # Check in database
            self.assertEqual(self.geokret1.holder, self.user4)

    def test_update_geokret_last_position(self):
        """Check Move Tasks: compute GeoKret last position"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_distances(self.geokret1.id)
            db.session.commit()

            # Check in database
            self.assertEqual(self.geokret1.last_position_id, None)

    def test_update_geokret_last_move(self):
        """Check Move Tasks: compute GeoKret last move"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_distances(self.geokret1.id)
            db.session.commit()

            # Check in database
            self.assertEqual(self.geokret1.last_move_id, self.move9.id)

    def test_update_country_and_altitude(self):
        """Check Move Tasks: update country and altitude"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_country_and_altitude(self.move1.id)
            db.session.commit()

            # Check in database
            move = Move.query.get(self.move1.id)
            self.assertEqual(move.country, 'FR')
            self.assertNotEqual(move.altitude, '720')
            self.assertEqual(move.altitude, 720)

    @request_context
    def test_update_country_and_altitude_errors(self):
        """Check Move Tasks: update country and altitude failing api"""

        # Check api error responses
        geokret = self.blend_geokret(created_on_datetime="2017-12-01T17:17:17")
        another_move = self.blend_move(type=MOVE_TYPE_DROPPED, geokret=geokret,
                                       author=self.user_2, moved_on_datetime="2017-12-01T17:17:17",
                                       latitude=42, longitude=42)
        # run the function
        update_move_country_and_altitude(another_move.id)

        # Check in database
        self.assertEqual(another_move.country, 'XYZ')
        self.assertEqual(another_move.altitude, '-2000')
