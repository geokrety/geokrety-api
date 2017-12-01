from app import current_app as app
from app.api.helpers.data_layers import MOVE_TYPES, MOVE_TYPES_COUNT
from app.models import db
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestMovesType(GeokretyTestCase):
    """Test Move-Types CRUD operations"""

    def _blend(self):
        """Create mocked User"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.commit()

    def test_create_authenticated_only(self):
        """Check MovesType: POST is forbidden"""
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "moves-types",
                    "attributes": {
                        "name": "Fly to the moon"
                    }
                }
            }
            self._send_post("/v1/moves-types", payload=payload, code=405)
            self._send_post("/v1/moves-types", payload=payload, code=405, user=self.admin)
            self._send_post("/v1/moves-types", payload=payload, code=405, user=self.user1)
            self._send_post("/v1/moves-types", payload=payload, code=405, user=self.user2)

    def test_get_moves_types_list(self):
        """ Check MovesType: GET moves-types list"""
        with app.test_request_context():
            self._blend()

            def check(response):
                self.assertEqual(len(response), MOVE_TYPES_COUNT)
                self.assertTrue('attributes' in response[0])
                self.assertTrue('name' in response[0]['attributes'])
                self.assertTrue('name' in response[1]['attributes'])
                self.assertTrue('name' in response[2]['attributes'])
                self.assertTrue('name' in response[3]['attributes'])
                self.assertTrue('name' in response[4]['attributes'])
                self.assertTrue('name' in response[5]['attributes'])

            response = self._send_get("/v1/moves-types", code=200, user=self.admin)['data']
            check(response)

            response = self._send_get("/v1/moves-types", code=200, user=self.user1)['data']
            check(response)

            response = self._send_get("/v1/moves-types", code=200, user=self.user2)['data']
            check(response)

    def test_get_moves_types_details(self):
        """ Check MovesType: GET moves-types details"""
        with app.test_request_context():
            self._blend()
            url = '/v1/moves-types/%d'

            def check(response, name):
                self.assertTrue('attributes' in response)
                self.assertTrue('name' in response['attributes'])
                self.assertEqual(response['attributes']['name'], name)

            for geokrety_type in MOVE_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in MOVE_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.admin)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in MOVE_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.user1)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in MOVE_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.user2)['data']
                check(response, geokrety_type['name'])

    def test_get_moves_types_unexistent(self):
        """ Check MovesType: GET moves-types unexistent"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/moves-types/666', code=404)
            self._send_get('/v1/moves-types/666', code=404, user=self.admin)
            self._send_get('/v1/moves-types/666', code=404, user=self.user1)
            self._send_get('/v1/moves-types/666', code=404, user=self.user2)

    def test_patch_list(self):
        """
        Check MovesType: PATCH list is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/moves-types", code=405)
            self._send_patch("/v1/moves-types", code=405, user=self.admin)
            self._send_patch("/v1/moves-types", code=405, user=self.user1)
            self._send_patch("/v1/moves-types", code=405, user=self.user2)

    def test_patch_forbidden(self):
        """
        Check MovesType: PATCH is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/moves-types/0", code=405)
            self._send_patch("/v1/moves-types/0", code=405, user=self.admin)
            self._send_patch("/v1/moves-types/0", code=405, user=self.user1)
            self._send_patch("/v1/moves-types/0", code=405, user=self.user2)

    def test_delete_list(self):
        """
        Check MovesType: DELETE list is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/moves-types", code=405)
            self._send_delete("/v1/moves-types", code=405, user=self.admin)
            self._send_delete("/v1/moves-types", code=405, user=self.user1)
            self._send_delete("/v1/moves-types", code=405, user=self.user2)

    def test_delete_forbidden(self):
        """
        Check Geokret: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/moves-types/0", code=405)
            self._send_delete("/v1/moves-types/0", code=405, user=self.admin)
            self._send_delete("/v1/moves-types/0", code=405, user=self.user1)
            self._send_delete("/v1/moves-types/0", code=405, user=self.user2)
