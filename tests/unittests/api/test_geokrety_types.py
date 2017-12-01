from app import current_app as app
from app.api.helpers.data_layers import GEOKRETY_TYPES, GEOKRETY_TYPES_COUNT
from app.models import db
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestGeokretyType(GeokretyTestCase):
    """Test GeoKrety-Types CRUD operations"""

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
        """Check GeokretyType: POST is forbidden"""
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "geokrety-types",
                    "attributes": {
                        "name": "A Car"
                    }
                }
            }
            self._send_post("/v1/geokrety-types", payload=payload, code=405)
            self._send_post("/v1/geokrety-types", payload=payload, code=405, user=self.admin)
            self._send_post("/v1/geokrety-types", payload=payload, code=405, user=self.user1)
            self._send_post("/v1/geokrety-types", payload=payload, code=405, user=self.user2)

    def test_get_geokrety_types_list(self):
        """ Check GeokretyType: GET geokrety-types list"""
        with app.test_request_context():
            self._blend()

            def check(response):
                self.assertEqual(len(response), GEOKRETY_TYPES_COUNT)
                self.assertTrue('attributes' in response[0])
                self.assertTrue('name' in response[0]['attributes'])
                self.assertTrue('name' in response[1]['attributes'])
                self.assertTrue('name' in response[2]['attributes'])
                self.assertTrue('name' in response[3]['attributes'])
                self.assertTrue('name' in response[4]['attributes'])

            response = self._send_get("/v1/geokrety-types", code=200, user=self.admin)['data']
            check(response)

            response = self._send_get("/v1/geokrety-types", code=200, user=self.user1)['data']
            check(response)

            response = self._send_get("/v1/geokrety-types", code=200, user=self.user2)['data']
            check(response)

    def test_get_geokrety_types_details(self):
        """ Check GeokretyType: GET geokrety-types details"""
        with app.test_request_context():
            self._blend()
            url = '/v1/geokrety-types/%d'

            def check(response, name):
                self.assertTrue('attributes' in response)
                self.assertTrue('name' in response['attributes'])
                self.assertEqual(response['attributes']['name'], name)

            for geokrety_type in GEOKRETY_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in GEOKRETY_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.admin)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in GEOKRETY_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.user1)['data']
                check(response, geokrety_type['name'])

            for geokrety_type in GEOKRETY_TYPES:
                response = self._send_get(url % geokrety_type['id'], code=200, user=self.user2)['data']
                check(response, geokrety_type['name'])

    def test_get_geokrety_types_unexistent(self):
        """ Check GeokretyType: GET geokrety-types unexistent"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/geokrety-types/666', code=404)
            self._send_get('/v1/geokrety-types/666', code=404, user=self.admin)
            self._send_get('/v1/geokrety-types/666', code=404, user=self.user1)
            self._send_get('/v1/geokrety-types/666', code=404, user=self.user2)

    def test_patch_list(self):
        """
        Check GeokretyType: PATCH list is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/geokrety-types", code=405)
            self._send_patch("/v1/geokrety-types", code=405, user=self.admin)
            self._send_patch("/v1/geokrety-types", code=405, user=self.user1)
            self._send_patch("/v1/geokrety-types", code=405, user=self.user2)

    def test_patch_forbidden(self):
        """
        Check GeokretyType: PATCH is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/geokrety-types/0", code=405)
            self._send_patch("/v1/geokrety-types/0", code=405, user=self.admin)
            self._send_patch("/v1/geokrety-types/0", code=405, user=self.user1)
            self._send_patch("/v1/geokrety-types/0", code=405, user=self.user2)

    def test_delete_list(self):
        """
        Check GeokretyType: DELETE list is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety-types", code=405)
            self._send_delete("/v1/geokrety-types", code=405, user=self.admin)
            self._send_delete("/v1/geokrety-types", code=405, user=self.user1)
            self._send_delete("/v1/geokrety-types", code=405, user=self.user2)

    def test_delete_forbidden(self):
        """
        Check Geokret: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety-types/0", code=405)
            self._send_delete("/v1/geokrety-types/0", code=405, user=self.admin)
            self._send_delete("/v1/geokrety-types/0", code=405, user=self.user1)
            self._send_delete("/v1/geokrety-types/0", code=405, user=self.user2)
