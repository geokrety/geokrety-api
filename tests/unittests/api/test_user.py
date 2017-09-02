import json

from app import current_app as app
from tests.unittests.utils import GeokretyTestCase
from app.models import db

class TestUser(GeokretyTestCase):

    def _check(self, payload, code, content_type='application/vnd.api+json'):
        with app.test_request_context():
            response = self.app.post('/v1/users',
                                     data=json.dumps(payload),
                                     content_type=content_type)
        self.assertEqual(response.status_code, code)

    def test_create_errors(self):
        self._check("not a json", 415, content_type='application/json')
        # self._check("not a json", 400, content_type='application/vnd.api+json')
        self._check({}, 422)
        self._check({"user": "kumy"}, 422)
        payload = {
            "data": {
                "type": "user"
            }
        }
        self._check(payload, 500)


    def test_user_create(self):

        # Test inserting first user
        payload = {
            "data": {
                "type": "user",
                "attributes": {
                    "name": "kumy"
                }
            }
        }
        self._check(payload, 201)

        # read it back
        response = self.app.get('/v1/users')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(data['data']), 1)
        self.assertTrue('attributes' in data['data'][0])
        self.assertTrue('name' in data['data'][0]['attributes'])
        self.assertEqual(data['data'][0]['attributes']['name'], "kumy")

        # Test inserting a second user
        payload = {
            "data": {
                "type": "user",
                "attributes": {
                    "name": "filips"
                }
            }
        }
        self._check(payload, 201)

        # read it back
        response = self.app.get('/v1/users')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['data']), 2)
        self.assertTrue('attributes' in data['data'][1])
        self.assertTrue('name' in data['data'][1]['attributes'])
        self.assertEqual(data['data'][1]['attributes']['name'], "filips")
