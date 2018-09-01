from app import current_app as app
from app.api.helpers.data_layers import GEOKRETY_TYPES, GEOKRETY_TYPES_LIST
from app.api.helpers.data_layers import GEOKRET_TYPE_TRADITIONAL, GEOKRET_TYPE_COIN
from app.models import db
from app.models.user import User
from app.models.geokret import Geokret
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
            self.geokret1 = mixer.blend(Geokret, type="0")
            self.geokret2 = mixer.blend(Geokret, type="3")
            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.add(self.geokret1)
            db.session.add(self.geokret2)
            db.session.commit()

    def test_create_is_forbidden(self):
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
                self.assertEqual(len(response), len(GEOKRETY_TYPES_LIST))
                self.assertEqual(len(response), len(GEOKRETY_TYPES))
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
            url = '/v1/geokrety-types/%s'

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

    def test_get_geokrety_type_details_from_geokret(self):
        """ Check GeokretyType: GET geokrety-type for a GeoKret"""
        with app.test_request_context():
            self._blend()
            url = '/v1/geokrety/%s/geokrety-types'

            def check(response, name):
                self.assertTrue('attributes' in response)
                self.assertTrue('name' in response['attributes'])
                self.assertEqual(response['attributes']['name'], name)

            response = self._send_get(url % self.geokret1.id, code=200)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_TRADITIONAL)]['name'])
            response = self._send_get(url % self.geokret2.id, code=200)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_COIN)]['name'])

            response = self._send_get(url % self.geokret1.id, code=200, user=self.admin)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_TRADITIONAL)]['name'])
            response = self._send_get(url % self.geokret2.id, code=200, user=self.admin)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_COIN)]['name'])

            response = self._send_get(url % self.geokret1.id, code=200, user=self.user1)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_TRADITIONAL)]['name'])
            response = self._send_get(url % self.geokret2.id, code=200, user=self.user1)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_COIN)]['name'])

            response = self._send_get(url % self.geokret1.id, code=200, user=self.user2)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_TRADITIONAL)]['name'])
            response = self._send_get(url % self.geokret2.id, code=200, user=self.user2)['data']
            check(response, GEOKRETY_TYPES[int(GEOKRET_TYPE_COIN)]['name'])

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
