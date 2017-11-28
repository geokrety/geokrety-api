from app import current_app as app
from app.models import db
from app.models.geokret import Geokret
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestUserGeokretyHeld(GeokretyTestCase):
    """Test User holding operations"""

    def _blend_users(self):
        """Create mocked Users"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            self.admin = mixer.blend(User, username="Admin 1")
            self.user1 = mixer.blend(User, username="Someone 1")
            self.user2 = mixer.blend(User, username="Someone 2")
            self.user3 = mixer.blend(User, username="Someone 3")
            self.user4 = mixer.blend(User, username="Someone 4")
            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.add(self.user3)
            db.session.add(self.user4)
            db.session.commit()

    def _blend(self):
        """Create mocked Geokret relationship"""
        with mixer.ctx(commit=False):
            self.geokret1 = mixer.blend(Geokret, owner=self.user1, holder=None)
            self.geokret2 = mixer.blend(Geokret, owner=self.user1, holder=self.user3)
            self.orphan_geokret1 = mixer.blend(Geokret, owner=None, holder=None)
            self.geokret3 = mixer.blend(Geokret, owner=self.user2, holder=None)
            self.geokret4 = mixer.blend(Geokret, owner=self.user2, holder=self.user3)
            self.orphan_geokret2 = mixer.blend(Geokret, owner=None, holder=self.user4)
            db.session.add(self.geokret1)
            db.session.add(self.geokret2)
            db.session.add(self.orphan_geokret1)
            db.session.add(self.geokret3)
            db.session.add(self.geokret4)
            db.session.add(self.orphan_geokret2)
            db.session.commit()

    def test_get_include_geokrety_held_user1(self):
        """Check TestUserGeokretyHeld: GET user include GeoKrety held - User1"""
        with app.test_request_context():
            self._blend_users()
            self._blend()
            url = '/v1/users/%d?include=geokrety-held' % self.user1.id

            response = self._send_get(url, code=200)
            self.assertFalse('included' in response)

            response = self._send_get(url, user=self.admin, code=200)
            self.assertFalse('included' in response)

            response = self._send_get(url, user=self.user1, code=200)
            self.assertFalse('included' in response)

            response = self._send_get(url, user=self.user2, code=200)
            self.assertFalse('included' in response)

            response = self._send_get(url, user=self.user3, code=200)
            self.assertFalse('included' in response)

            response = self._send_get(url, user=self.user4, code=200)
            self.assertFalse('included' in response)

    def test_get_include_geokrety_held_user3(self):
        """Check TestUserGeokretyHeld: GET user include GeoKrety held - User3"""
        with app.test_request_context():
            self._blend_users()
            self._blend()
            url = '/v1/users/%d?include=geokrety-held' % self.user3.id

            response = self._send_get(url, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)

            response = self._send_get(url, user=self.admin, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)

            response = self._send_get(url, user=self.user1, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)

            response = self._send_get(url, user=self.user2, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)

            response = self._send_get(url, user=self.user3, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)

            response = self._send_get(url, user=self.user4, code=200)['included']
            self.assertEqual(len(response), 2)
            self._check_geokret(response[0], self.geokret4)
            self._check_geokret(response[1], self.geokret2)
