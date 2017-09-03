import unittest
import json

from tests.unittests.setup_database import Setup

from app import current_app as app
from app.models import db
from app.factories.user import UserFactory


class GeokretyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def tearDown(self):
        Setup.drop_db()

    def _login(self, username="kumy", password="password", create=False):
        """
        Obtain a JWT token to authenticate next requests
        """
        if create:
            with app.test_request_context():
                user = UserFactory(name=username, password=password)
                db.session.add(user)
                db.session.commit()

        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": username,
                                     "password": password
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        raised = False
        try:
            data = json.loads(response.data)
        except Exception:
            raised = True
        self.assertFalse(raised, 'Failed to decode json')
        self.assertTrue('access_token' in data)
        return data['access_token']

    def _add_auth_header(self, headers, user="kumy", password="password", create=False):
        """
        Add authentication header
        """
        headers['Authorization'] = \
            'JWT %s' % self._login(user, password, create=create)
        return headers

    def _send_post(self, endpoint, payload=None, code=200, user="kumy", password="password", content_type='application/vnd.api+json', auth=False, create=False):
        """
        Send a POST request to the api, and check expected response code.
        Properly set content-type
        Also add an authentication token by default
        """
        if not payload:
            payload = {}

        headers = {}
        if auth:
            headers = self._add_auth_header(
                headers, user=user, password=password, create=create)

        with app.test_request_context():
            response = self.app.post(endpoint,
                                     data=json.dumps(payload),
                                     headers=headers,
                                     content_type=content_type)
        self.assertEqual(response.status_code, code)
        return response

    def _send_get(self, endpoint, code=200, user="kumy", password="password", auth=False, create=False):
        """
        Send a POST request to the api, and check expected response code.
        Properly set content-type
        Also add an authentication token by default
        """
        headers = {}
        if auth:
            headers = self._add_auth_header(
                headers, user=user, password=password, create=create)

        with app.test_request_context():
            response = self.app.get(endpoint,
                                    headers=headers)
        self.assertEqual(response.status_code, code)
        return response

    def _send_delete(self, endpoint, payload=None, code=200, user="kumy", password="password", auth=False, create=False):
        """
        Send a DELETE request to the api, and check expected response code.
        Properly set content-type
        Also add an authentication token by default
        """
        headers = {}
        if auth:
            headers = self._add_auth_header(
                headers, user=user, password=password, create=create)

        with app.test_request_context():
            response = self.app.delete(endpoint,
                                       data=json.dumps(payload),
                                       headers=headers)
        self.assertEqual(response.status_code, code)
        return response

    def _send_patch(self, endpoint, payload=None, code=200, content_type='application/vnd.api+json', user="kumy", password="password", auth=False, create=False):
        """
        Send a PATCH request to the api, and check expected response code.
        Properly set content-type
        Also add an authentication token by default
        """
        headers = {}
        if auth:
            headers = self._add_auth_header(
                headers, user=user, password=password, create=create)

        with app.test_request_context():
            response = self.app.patch(endpoint,
                                      data=json.dumps(payload),
                                      headers=headers,
                                      content_type=content_type)
        self.assertEqual(response.status_code, code)
        return response

    def _check_commit_and_raise(self, obj, exc):
        with app.test_request_context():
            db.session.add(obj)

            with self.assertRaises(exc):
                db.session.commit()
            db.session.rollback()

    def _check_commit_and_not_raise(self, obj):
        with app.test_request_context():
            raised = False
            try:
                db.session.commit()
            except Exception:
                raised = True
            self.assertFalse(raised, 'Exception raised when it should not')

            db.session.rollback()
