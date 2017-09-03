import json

from app import current_app as app
from app.models import db
from app.factories.user import UserFactory
from tests.unittests.utils import GeokretyTestCase


class TestAuthentication(GeokretyTestCase):
    username = "kumy"
    password = "password"
    password_bad = "bad_password"

    def test_auth_nonexistent_user(self):
        """
        Check can't login with non-existent user
        """

        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": self.username,
                                     "password": self.password
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 401)

    def test_auth(self):
        """
        Check can login with existent user
        """

        with app.test_request_context():
            user = UserFactory(name=self.username, password=self.password)
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": self.username,
                                     "password": self.password
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_auth_bad_password(self):
        """
        Check can't login with bad password
        """

        with app.test_request_context():
            user = UserFactory(name=self.username, password=self.password)
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": self.username,
                                     "password": self.password_bad
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 401)

    def test_auth_bad_username(self):
        """
        Check can't login with bad username
        """

        with app.test_request_context():
            user = UserFactory(name=self.username, password=self.password)
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": self.username+"_bad",
                                     "password": self.password
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 401)
