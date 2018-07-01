import responses
from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED,
                                         MOVE_TYPE_SEEN)
from app.api.helpers.move_tasks import (update_country_and_altitude,
                                        update_move_distances)
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestMoveTasksHelper(GeokretyTestCase):

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
                                        created_on_date_time="2017-12-01T14:18:22")

            # Moves
            self.move1 = mixer.blend(Move, move_type_id=MOVE_TYPE_DROPPED, geokret=self.geokret1,
                                     author=self.user2, moved_on_date_time="2017-12-01T14:21:22",
                                     latitude=43.694483, longitude=6.85575)
            self.move2 = mixer.blend(Move, move_type_id=MOVE_TYPE_COMMENT, geokret=self.geokret1,
                                     author=self.user1, moved_on_date_time="2017-12-01T14:24:22")
            self.move3 = mixer.blend(Move, move_type_id=MOVE_TYPE_DIPPED, geokret=self.geokret1,
                                     author=self.user4, moved_on_date_time="2017-12-01T14:25:22",
                                     latitude=43.704233, longitude=6.869833)
            self.move4 = mixer.blend(Move, move_type_id=MOVE_TYPE_DIPPED, geokret=self.geokret1,
                                     author=self.user4, moved_on_date_time="2017-12-01T14:23:22",
                                     latitude=43.6792, longitude=6.852933)
            self.move5 = mixer.blend(Move, move_type_id=MOVE_TYPE_SEEN, geokret=self.geokret1,
                                     author=self.user3, moved_on_date_time="2017-12-01T14:22:22",
                                     latitude=43.701767, longitude=6.84085)
            self.move6 = mixer.blend(Move, move_type_id=MOVE_TYPE_GRABBED, geokret=self.geokret1,
                                     author=self.user2, moved_on_date_time="2017-12-01T14:19:22")
            self.move7 = mixer.blend(Move, move_type_id=MOVE_TYPE_COMMENT, geokret=self.geokret1,
                                     author=self.user2, moved_on_date_time="2017-12-01T14:20:22")
            self.move8 = mixer.blend(Move, move_type_id=MOVE_TYPE_DROPPED, geokret=self.geokret1,
                                     author=self.user1, moved_on_date_time="2017-12-01T14:18:22",
                                     latitude=43.693633, longitude=6.860933)

    def test_update_move_distances(self):
        """Check Move Tasks: compute move distances"""

        with app.test_request_context():
            self._blend()

            # run the function
            update_move_distances(self.geokret1.id)
            db.session.commit()

            # Check in database
            moves = Move.query.filter(Move.geokret_id == self.geokret1.id) \
                .order_by(Move.moved_on_date_time.asc()).all()
            self.assertEqual(moves[0].distance, 0)
            self.assertEqual(moves[1].distance, 0)
            self.assertEqual(moves[2].distance, 0)
            self.assertEqual(moves[3].distance, int(round(0.428142805874)))
            self.assertEqual(moves[4].distance, int(round(1.44869620611)))
            self.assertEqual(moves[5].distance, int(round(2.69014884056)))
            self.assertEqual(moves[6].distance, 0)
            self.assertEqual(moves[7].distance, int(round(3.09681445874)))

    @responses.activate
    def test_update_country_and_altitude(self):
        """Check Move Tasks: update country and altitude"""

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=43.69448&lon=6.85575',
                      status=200, body='FR')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=43.69448&lon=6.85575',
                      status=200, body='720')

        with app.test_request_context():
            self._blend()

            # run the function
            update_country_and_altitude(self.move1.id)
            db.session.commit()

            # Check in database
            move = Move.query.get(self.move1.id)
            self.assertEqual(move.country, 'FR')
            self.assertNotEqual(move.altitude, '720')
            self.assertEqual(move.altitude, 720)

    @responses.activate
    def test_update_country_and_altitude_errors(self):
        """Check Move Tasks: update country and altitude failing api"""

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=0&lon=0',
                      status=400)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=0&lon=0',
                      status=500)

        with app.test_request_context():
            self._blend()

            # Check api error responses
            another_move = mixer.blend(Move, move_type_id=MOVE_TYPE_DROPPED, geokret=self.geokret1,
                                       author=self.user2, moved_on_date_time="2017-12-01T17:17:17",
                                       latitude=0, longitude=0)
            # run the function
            update_country_and_altitude(another_move.id)
            db.session.commit()

            # Check in database
            move = Move.query.get(another_move.id)
            self.assertEqual(move.country, 'XYZ')
            self.assertNotEqual(move.altitude, '-2000')
            self.assertEqual(move.altitude, -2000)
