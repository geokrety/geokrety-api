# coding=utf-8
import datetime

import responses
from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_COIN, GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase, MovePayload, ResponsesMixin


class TestMove(ResponsesMixin, GeokretyTestCase):
    """Test Move CRUD operations"""

    def _blend(self):
        """Create mocked Geokret/User"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            # Users
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            self.user3 = mixer.blend(User)

            # GeoKrety
            self.geokret1 = mixer.blend(Geokret, type=GEOKRET_TYPE_TRADITIONAL,
                                        owner=self.user1, holder=self.user2, tracking_code="ABC123",
                                        created_on_date_time="2017-12-01T14:18:22")
            self.geokret2 = mixer.blend(Geokret, type=GEOKRET_TYPE_TRADITIONAL, owner=self.user2, holder=self.user1,
                                        created_on_date_time="2017-12-01T14:18:22")
            self.geokret3 = mixer.blend(Geokret, type=GEOKRET_TYPE_HUMAN,
                                        created_on_date_time="2017-12-01T14:18:22")
            self.geokret4 = mixer.blend(Geokret, type=GEOKRET_TYPE_COIN,
                                        created_on_date_time="2017-12-01T14:18:22")
            self.geokret5 = mixer.blend(Geokret, type=GEOKRET_TYPE_COIN,
                                        created_on_date_time="2017-12-01T14:18:22")

            # Moves
            self.move1 = mixer.blend(Move, id=1, move_type_id=MOVE_TYPE_DROPPED, latitude=43.78,
                                     longitude=7.06, geokret=self.geokret1, author=self.user1)
            self.move2 = mixer.blend(Move, id=2, move_type_id=MOVE_TYPE_GRABBED,
                                     geokret=self.geokret1, author=self.user2)
            self.move3 = mixer.blend(Move, id=3, move_type_id=MOVE_TYPE_COMMENT, geokret=self.geokret2, author=None)
            self.move4 = mixer.blend(Move, id=4, move_type_id=MOVE_TYPE_SEEN, latitude=43.78,
                                     longitude=7.06, geokret=self.geokret2, author=None)
            self.move5 = mixer.blend(Move, id=5, move_type_id=MOVE_TYPE_ARCHIVED, geokret=self.geokret2, author=None)
            self.move6 = mixer.blend(Move, id=6, move_type_id=MOVE_TYPE_DIPPED, latitude=43.78,
                                     longitude=7.06, geokret=self.geokret2, author=None)

            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.add(self.user3)
            db.session.add(self.geokret1)
            db.session.add(self.geokret2)
            db.session.add(self.geokret3)
            db.session.add(self.geokret4)
            db.session.add(self.geokret5)
            db.session.add(self.move1)
            db.session.add(self.move2)
            db.session.add(self.move3)
            db.session.add(self.move4)
            db.session.add(self.move5)
            db.session.add(self.move6)
            db.session.commit()

    def test_get_moves_list(self):
        """ Check Move: GET moves list """
        with app.test_request_context():
            self._blend()

            url = '/v1/moves'

            def check(response):
                self.assertEqual(len(response), 6)
                self._check_move(response[self.move1.id - 1], self.move1)
                self._check_move(response[self.move2.id - 1], self.move2)
                self._check_move(response[self.move3.id - 1], self.move3)
                self._check_move(response[self.move4.id - 1], self.move4)
                self._check_move(response[self.move5.id - 1], self.move5)
                self._check_move(response[self.move6.id - 1], self.move6)

            response = self._send_get(url, code=200)['data']
            check(response)

            response = self._send_get(url, code=200, user=self.admin)['data']
            check(response)

            response = self._send_get(url, code=200, user=self.user1)['data']
            check(response)

            response = self._send_get(url, code=200, user=self.user2)['data']
            check(response)

    def test_get_move_details_anonymous(self):
        """ Check Move: GET move details - Anonymous """
        with app.test_request_context():
            self._blend()

            url = '/v1/moves/%d'

            response = self._send_get(url % self.move1.id, code=200)
            self._check_move(response['data'], self.move1)

            response = self._send_get(url % self.move2.id, code=200)
            self._check_move(response['data'], self.move2)

            response = self._send_get(url % self.move3.id, code=200)
            self._check_move(response['data'], self.move3)

            self._send_get(url % 666, code=404)

    def test_get_move_details_admin(self):
        """ Check Move: GET move details - Admin """
        with app.test_request_context():
            self._blend()

            url = '/v1/moves/%d'

            response = self._send_get(url % self.move1.id, code=200, user=self.admin)
            self._check_move(response['data'], self.move1)

            response = self._send_get(url % self.move2.id, code=200, user=self.admin)
            self._check_move(response['data'], self.move2)

            response = self._send_get(url % self.move3.id, code=200, user=self.admin)
            self._check_move(response['data'], self.move3)

            self._send_get(url % 666, code=404, user=self.admin)

    def test_get_move_details_user1(self):
        """ Check Move: GET move details - User1 """
        with app.test_request_context():
            self._blend()

            url = '/v1/moves/%d'

            response = self._send_get(url % self.move1.id, code=200, user=self.user1)
            self._check_move(response['data'], self.move1)

            response = self._send_get(url % self.move2.id, code=200, user=self.user1)
            self._check_move(response['data'], self.move2)

            response = self._send_get(url % self.move3.id, code=200, user=self.user1)
            self._check_move(response['data'], self.move3)

            self._send_get(url % 666, code=404, user=self.user1)

    def test_get_move_details_user2(self):
        """ Check Move: GET move details - User2 """
        with app.test_request_context():
            self._blend()

            url = '/v1/moves/%d'

            response = self._send_get(url % self.move1.id, code=200, user=self.user2)
            self._check_move(response['data'], self.move1)

            response = self._send_get(url % self.move2.id, code=200, user=self.user2)
            self._check_move(response['data'], self.move2)

            response = self._send_get(url % self.move3.id, code=200, user=self.user2)
            self._check_move(response['data'], self.move3)

            self._send_get(url % 666, code=404, user=self.user2)

    def test_invalid_move_type(self):
        """Check Move: POST Invalid move type
        """
        with app.test_request_context():
            self._blend()

            self._send_post("/v1/moves", payload=MovePayload(move_type=-1), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(666), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type="-1"), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type="666"), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type="A"), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type=""), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type=" "), code=422, user=self.admin)
            self._send_post("/v1/moves", payload=MovePayload(move_type=u"Póki"), code=422, user=self.admin)

    def test_geokret_id_in_response(self):
        """Check Move: POST GeoKret ID have to be present
        """
        with app.test_request_context():
            self._blend()

            payload = MovePayload(move_type=MOVE_TYPE_DROPPED) \
                .tracking_code(self.geokret1.tracking_code) \
                .coordinates()
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            # Check in response
            self.assertIn('geokret-id', response['data']['attributes'])
            self.assertEqual(self.geokret1.id, response['data']['attributes']['geokret-id'])

            # Check in database
            move = Move.query.filter(Move.id == response["data"]["id"]).one()
            self.assertIsNotNone(move.geokret_id)

    def test_create_validate_coordinates(self):
        """Check Move: POST validate coordinates"""
        with app.test_request_context():
            self._blend()
            payload = MovePayload(move_type=MOVE_TYPE_DROPPED).tracking_code()

            # Coordinates missing
            self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

            # Valid coordinates
            payload.coordinates()
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
            self._check_move(response['data'], payload.blend(), skip_check=['times'])

            valid_latitudes = ['0', '90', '+90.0', '-90']
            valid_longitudes = ['0', '180', '+180', '-180']
            invalid_latitudes = ['91', '+91.0', '91']
            invalid_longitudes = ['181', '+181.0', '181']

            for latitude in valid_latitudes:
                payload.coordinates(latitude=latitude, longitude="0")
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            for longitude in valid_longitudes:
                payload.coordinates(latitude="0", longitude=longitude)
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            for latitude in invalid_latitudes:
                payload.coordinates(latitude=latitude, longitude="0")
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

            for longitude in invalid_longitudes:
                payload.coordinates(latitude="0", longitude=longitude)
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

    def _create_require_tracking_code_coordinates(self, move_type):
        """ Require:
                * tracking code
                * coordinates
        """
        with app.test_request_context():
            self._blend()

            # Anonymous Incomplete cases
            user = None
            payload = MovePayload(move_type)
            self._send_post("/v1/moves", payload=payload, code=422, user=user)

            payload = MovePayload(move_type).coordinates()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code("ABC123")
            self._send_post("/v1/moves", payload=payload, code=422, user=user)

            payload = MovePayload(move_type).tracking_code("666666")
            self._send_post("/v1/moves", payload=payload, code=422, user=user)

            payload = MovePayload(move_type).coordinates().tracking_code()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).username()
            self._send_post("/v1/moves", payload=payload, code=422, user=user)

            payload = MovePayload(move_type).coordinates().username()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code().username()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code("666666").username()
            self._send_post("/v1/moves", payload=payload, code=422, user=user)

            # Authenticated Incomplete cases
            for user in (self.admin, self.user1, self.user2):
                payload = MovePayload(move_type)
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

                payload = MovePayload(move_type).coordinates()
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

                payload = MovePayload(move_type).tracking_code()
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

                payload = MovePayload(move_type).tracking_code("666666")
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

            # Valid and Anonymous
            payload = MovePayload(move_type).coordinates().tracking_code().username()
            response = self._send_post("/v1/moves", payload=payload, code=201)
            self._check_move(response['data'], payload.blend(), skip_check=['times'])

            # Valid and Authenticated
            for user in (self.admin, self.user1, self.user2):
                payload = MovePayload(move_type).coordinates().tracking_code()
                response = self._send_post("/v1/moves", payload=payload, code=201, user=user)
                self._check_move(response['data'], payload.blend(), skip_check=['times'])

                payload.username()
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201)
                self._check_move(response['data'], payload.blend(), skip_check=['times'])

    def _create_require_tracking_code(self, move_type):
        """ Require:
                * tracking code
        """
        with app.test_request_context():
            self._blend()

            # Anonymous Incomplete cases
            payload = MovePayload(move_type)
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).coordinates()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code("666666")
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).coordinates().tracking_code()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).username()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).coordinates().username()
            self._send_post("/v1/moves", payload=payload, code=422)

            payload = MovePayload(move_type).tracking_code("666666").username()
            self._send_post("/v1/moves", payload=payload, code=422)

            # Authenticated Incomplete cases
            for user in (self.admin, self.user1, self.user2):
                payload = MovePayload(move_type)
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

                payload = MovePayload(move_type).coordinates()
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

                payload = MovePayload(move_type).tracking_code("666666")
                self._send_post("/v1/moves", payload=payload, code=422, user=user)

            # Valid and Anonymous
            payload = MovePayload(move_type).tracking_code().username()
            response = self._send_post("/v1/moves", payload=payload, code=201)
            self._check_move(response['data'], payload.blend(), skip_check=['times'])

            # Valid and Authenticated
            for user in (self.admin, self.user1, self.user2):
                payload = MovePayload(move_type).tracking_code()
                response = self._send_post("/v1/moves", payload=payload, code=201, user=user)
                self._check_move(response['data'], payload.blend(), skip_check=['times'])

                payload.username()
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201)
                self._check_move(response['data'], payload.blend(), skip_check=['times'])

    def test_create_type_dropped(self):
        """Check Move: POST check MOVE_TYPE_DROPPED properties
            * require:
                * coordinates
                * tracking code
        """

        self._create_require_tracking_code_coordinates(MOVE_TYPE_DROPPED)

    def test_create_type_grabbed(self):
        """Check Move: POST check MOVE_TYPE_GRABBED properties
            * require:
                * tracking code
            * exclude:
                * coordinates
        """
        self._create_require_tracking_code(MOVE_TYPE_GRABBED)

    def test_create_type_comment(self):
        """Check Move: POST check MOVE_TYPE_COMMENT properties
            * require:
                * tracking code
            * exclude:
                * coordinates
        """
        self._create_require_tracking_code(MOVE_TYPE_COMMENT)

    def test_create_type_dipped(self):
        """Check Move: POST check MOVE_TYPE_DIPPED properties
            * require:
                * tracking code
                * coordinates
        """

        self._create_require_tracking_code_coordinates(MOVE_TYPE_DIPPED)

    def test_create_type_seen(self):
        """Check Move: POST check MOVE_TYPE_SEEN properties
            * require:
                * tracking code
                * coordinates
        """
        self._create_require_tracking_code_coordinates(MOVE_TYPE_SEEN)

    def test_create_type_archived(self):
        """Check Move: POST check MOVE_TYPE_ARCHIVED properties
            * require:
                * tracking code
            Only admin or owner can archive a GeoKret
        """
        with app.test_request_context():
            self._blend()
            move_type = MOVE_TYPE_ARCHIVED

            payload = MovePayload(move_type).tracking_code(self.geokret1.tracking_code)
            self._send_post("/v1/moves", payload=payload, code=401, user=None)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.user1)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user2)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user3)

            payload = MovePayload(move_type).tracking_code(self.geokret2.tracking_code)
            self._send_post("/v1/moves", payload=payload, code=401, user=None)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user1)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.user2)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user3)

            payload = MovePayload(move_type).tracking_code(self.geokret3.tracking_code)
            self._send_post("/v1/moves", payload=payload, code=401, user=None)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user1)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user2)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=403, user=self.user3)

            payload = MovePayload(move_type).tracking_code("666666")
            self._send_post("/v1/moves", payload=payload, code=422, user=None)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=422, user=self.user1)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=422, user=self.user2)
            payload.moved_date_time()
            self._send_post("/v1/moves", payload=payload, code=422, user=self.user3)

    def test_create_move_date_is_mandatory(self):
        """Check Move: POST move date is mandatory"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.username()
                for user in (None, self.admin, self.user1, self.user2):
                    payload.moved_date_time()
                    self._send_post("/v1/moves", payload=payload, code=201, user=user)

                # payload.moved_date_time(None)
                del payload['data']['attributes']['moved_on_date_time']
                for user in (None, self.admin, self.user1, self.user2):
                    self._send_post("/v1/moves", payload=payload, code=422, user=user)

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_missing_move_date_defaults_to_now(self):
        """Check Move: POST missing move date is set to NOW()"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.username()
                for user in (None, self.admin, self.user1, self.user2):
                    payload.moved_date_time()
                    self._send_post("/v1/moves", payload=payload, code=201, user=user)

                del payload['data']['attributes']['moved_on_date_time']
                for user in (None, self.admin, self.user1, self.user2):
                    payload.moved_date_time()
                    result = self._send_post("/v1/moves", payload=payload, code=201, user=user)
                    self.assertIsNotNone(result['data']['attributes']['moved-on-date-time'])

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_identical_move_date_is_forbidden(self):
        """Check Move: POST identical move date is forbidden"""
        with app.test_request_context():
            self._blend()

            payload = MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code(self.geokret1.tracking_code)
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            # Check in database
            move = Move.query.filter(Move.id == response["data"]["id"]).one()
            self.assertFalse(len(move.username))

            self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

    def test_comment_encoding(self):
        """Check Move: Validate comment encoding
        """
        with app.test_request_context():
            self._blend()
            _raw = u"Póki"
            _enc = "P&oacute;ki"

            # Post some data wich will be encoded for html entities
            payload = MovePayload(MOVE_TYPE_DIPPED) \
                .coordinates() \
                .tracking_code() \
                .comment(_raw)
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
            self._check_move(response['data'], payload.blend(), skip_check=['times'])

            move = Move.query.filter(Move.id == response["data"]["id"]).one()
            # Read raw database field
            self.assertEqual(move._comment, _enc)
            # Read unencoded database field
            self.assertEqual(move.comment, _raw)
            # Read value via API
            response = self._send_get("/v1/moves/%s" % move.id, code=200, user=self.admin)
            self.assertEqual(response["data"]["attributes"]["comment"], _raw)

    def test_create_username_required_for_anonymous(self):
        """Check Move: POST username required for anonymous"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.moved_date_time()
                # Admin checks
                response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

                # Check in database
                move = Move.query.filter(Move.id == response["data"]["id"]).one()
                self.assertFalse(len(move.username))

                # Anonymous checks
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=422)
                payload.username()
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201)

                # Check in database
                move = Move.query.filter(Move.id == response["data"]["id"]).one()
                self.assertEqual(move.username, payload["data"]['attributes']["username"])

                # Read value via API
                response = self._send_get("/v1/moves/%s" % move.id, code=200, user=self.admin)
                self.assertEqual(response["data"]["attributes"]["username"], move.username)

                # Authenticated
                for user in (self.admin, self.user1, self.user2):
                    payload.moved_date_time()
                    response = self._send_post("/v1/moves", payload=payload, code=201, user=user)

                    # Check in database
                    move = Move.query.filter(Move.id == response["data"]["id"]).one()
                    self.assertFalse(len(move.username))

                    # Read value via API
                    response = self._send_get("/v1/moves/%s" % move.id, code=200, user=self.admin)
                    self.assertTrue("username" in response["data"]["attributes"])
                    self.assertFalse(len(response["data"]["attributes"]["username"]))

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_author_id_force_connected_user_as_author(self):
        """Check Move: POST force current connected user as author"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                self._send_post("/v1/moves", payload=payload, code=422)
                payload.username()
                payload.moved_date_time()
                response = self._send_post("/v1/moves", payload=payload, code=201)

                # Check in database
                move = Move.query.filter(Move.id == response["data"]["id"]).one()
                self.assertEqual(move.author_id, None)

                # Read value via API
                response = self._send_get("/v1/moves/%s?include=author" % move.id, code=200, user=self.admin)
                self.assertEqual(response["data"]["relationships"]["author"]["data"], None)

                # Authenticated
                for user in (self.admin, self.user1, self.user2):
                    payload.moved_date_time()
                    response = self._send_post("/v1/moves", payload=payload, code=201, user=user)

                    # Check in database
                    move = Move.query.filter(Move.id == response["data"]["id"]).one()
                    self.assertEqual(move.author_id, user.id)

                    # Read value via API
                    response = self._send_get("/v1/moves/%s?include=author" % move.id, code=200, user=self.admin)
                    self.assertNotEqual(response["data"]["relationships"]["author"]["data"], None)
                    self.assertEqual(response["data"]["relationships"]["author"]["data"]["id"], str(user.id))

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_author_relationship_override_only_by_admins(self):
        """Check Move: POST author relationship overridable only by admin"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.author_relationship(self.user1.id)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403, user=self.user1)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403, user=self.user2)

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_author_id_override_only_by_admins(self):
        """Check Move: POST author_id overridable only by admin"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.author_id(self.user1.id)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403, user=self.user1)
                payload.moved_date_time()
                self._send_post("/v1/moves", payload=payload, code=403, user=self.user2)

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code())
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code())
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code())
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code())

    def test_create_forbid_move_before_birth_date(self):
        """Check Move: POST forbidden for move before birth date"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.username()

                # yesterday
                datetime_obj = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

                # 1 day before GeoKret birth
                datetime_obj = (self.geokret1.created_on_date_time -
                                datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

                # 1 second before GeoKret birth
                datetime_obj = (self.geokret1.created_on_date_time -
                                datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

                # Same time as GeoKret birth
                payload.moved_date_time(self.geokret1.created_on_date_time.strftime("%Y-%m-%dT%H:%M:%S"))
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

                # now
                datetime_obj = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code(self.geokret1.tracking_code))
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code(self.geokret2.tracking_code))
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code(self.geokret3.tracking_code))
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code(self.geokret4.tracking_code))
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code(self.geokret5.tracking_code))

    def test_create_forbid_move_in_the_future(self):
        """Check Move: POST forbidden for move in the future"""
        with app.test_request_context():
            self._blend()

            def check(payload):
                payload.username()

                # yesterday
                datetime_obj = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

                # tomorrow
                datetime_obj = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

                # in 1 minute
                datetime_obj = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
                                ).strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=422, user=self.admin)

                # now
                datetime_obj = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                payload.moved_date_time(datetime_obj)
                self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            check(MovePayload(MOVE_TYPE_DROPPED).coordinates().tracking_code(self.geokret1.tracking_code))
            check(MovePayload(MOVE_TYPE_GRABBED).tracking_code(self.geokret2.tracking_code))
            check(MovePayload(MOVE_TYPE_COMMENT).tracking_code(self.geokret3.tracking_code))
            check(MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code(self.geokret4.tracking_code))
            check(MovePayload(MOVE_TYPE_SEEN).coordinates().tracking_code(self.geokret5.tracking_code))

    def test_update_country_elevation(self):
        """Check Move: POST move will be amended with country and elevation"""
        with app.test_request_context():
            self._blend()

            payload = MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code()
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            self.assertEqual(response['data']['attributes']['country'], '')
            self.assertEqual(response['data']['attributes']['altitude'], -32768)

            # Check in database
            move = Move.query.filter(Move.id == response["data"]["id"]).one()
            self.assertEqual(move.country, 'FR')
            self.assertEqual(move.altitude, 720)

    def test_update_distances(self):
        """Check Move: POST moves will be amended with updated distances"""
        with app.test_request_context():
            self._blend()

            # insert first move
            payload = MovePayload(MOVE_TYPE_DIPPED).coordinates().tracking_code()
            self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            # insert second move
            payload = payload.coordinates(48.8567, 2.3508).moved_date_time()
            response = self._send_post("/v1/moves", payload=payload, code=201, user=self.admin)

            self.assertEqual(response['data']['attributes']['distance'], 0)

            # Check in database
            move = Move.query.filter(Move.id == response["data"]["id"]).one()
            self.assertEqual(move.distance, 670)

    def test_delete_list(self):
        """
        Check Move: DELETE list
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/moves", code=405)
            self._send_delete("/v1/moves", code=405, user=self.admin)
            self._send_delete("/v1/moves", code=405, user=self.user1)
            self._send_delete("/v1/moves", code=405, user=self.user2)

    def test_delete_unexistent_move(self):
        """
        Check Move: DELETE Unexistent move
        """
        with app.test_request_context():
            self._blend()
            url = '/v1/moves/%d'

            self._send_delete(url % 666, code=401, user=None)
            self._send_delete(url % 666, code=404, user=self.admin)
            self._send_delete(url % 666, code=404, user=self.user1)
            self._send_delete(url % 666, code=404, user=self.user2)

    def test_delete_anonymous(self):
        """
        Check Move: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend()
            url = '/v1/moves/%d'

            self._send_delete(url % self.move1.id, code=401)
            self._send_delete(url % self.move2.id, code=401)
            self._send_delete(url % self.move3.id, code=401)

    def test_delete_admin(self):
        """
        Check Move: DELETE Admin
        """
        with app.test_request_context():
            self._blend()
            url = '/v1/moves/%d'

            self._send_delete(url % self.move1.id, code=200, user=self.admin)
            self._send_delete(url % self.move2.id, code=200, user=self.admin)
            self._send_delete(url % self.move3.id, code=200, user=self.admin)

    def test_delete_user1(self):
        """
        Check Move: DELETE User1
        """
        with app.test_request_context():
            self._blend()
            url = '/v1/moves/%d'

            self._send_delete(url % self.move1.id, code=200, user=self.user1)
            self._send_delete(url % self.move2.id, code=403, user=self.user1)
            self._send_delete(url % self.move3.id, code=403, user=self.user1)

    def test_delete_user2(self):
        """
        Check Move: DELETE User2
        """
        with app.test_request_context():
            self._blend()
            url = '/v1/moves/%d'

            self._send_delete(url % self.move1.id, code=403, user=self.user2)
            self._send_delete(url % self.move2.id, code=200, user=self.user2)
            self._send_delete(url % self.move3.id, code=403, user=self.user2)
