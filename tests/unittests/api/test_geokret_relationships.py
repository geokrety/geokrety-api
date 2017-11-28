from app import current_app as app
from app.models import db
from app.models.geokret import Geokret
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestGeokretRelationships(GeokretyTestCase):
    """Test Geokret CRUD operations"""

    def _blend_users(self):
        """Create mocked Users"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            self.user3 = mixer.blend(User)
            self.user4 = mixer.blend(User)
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

    def test_get_geokrety_owned_status_codes(self):
        """Check GeokretRelationships: GET geokrety-owned - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_get('/v1/users/1/relationship/geokrety-owned', code=200)
            self._send_get('/v1/users/1/relationship/geokrety-owned', code=200, user=self.admin)
            self._send_get('/v1/users/1/relationship/geokrety-owned', code=200, user=self.user1)
            self._send_get('/v1/users/1/relationship/geokrety-owned', code=200, user=self.user2)

    def test_post_geokrety_owned_status_codes(self):
        """Check GeokretRelationships: POST geokrety-owned - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_post('/v1/users/1/relationship/geokrety-owned', code=405)
            self._send_post('/v1/users/1/relationship/geokrety-owned', code=405, user=self.admin)
            self._send_post('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user1)
            self._send_post('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user2)

    def test_patch_geokrety_owned_status_codes(self):
        """Check GeokretRelationships: PATCH geokrety-owned - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_patch('/v1/users/1/relationship/geokrety-owned', code=405)
            self._send_patch('/v1/users/1/relationship/geokrety-owned', code=405, user=self.admin)
            self._send_patch('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user1)
            self._send_patch('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user2)

    def test_delete_geokrety_owned_status_codes(self):
        """Check GeokretRelationships: DELETE geokrety-owned - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_delete('/v1/users/1/relationship/geokrety-owned', code=405)
            self._send_delete('/v1/users/1/relationship/geokrety-owned', code=405, user=self.admin)
            self._send_delete('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user1)
            self._send_delete('/v1/users/1/relationship/geokrety-owned', code=405, user=self.user2)

    def test_get_geokrety_held_status_codes(self):
        """Check GeokretRelationships: GET geokrety-held - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_get('/v1/users/1/relationship/geokrety-held', code=200)
            self._send_get('/v1/users/1/relationship/geokrety-held', code=200, user=self.admin)
            self._send_get('/v1/users/1/relationship/geokrety-held', code=200, user=self.user1)
            self._send_get('/v1/users/1/relationship/geokrety-held', code=200, user=self.user2)

    def test_post_geokrety_held_status_codes(self):
        """Check GeokretRelationships: POST geokrety-held - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_post('/v1/users/1/relationship/geokrety-held', code=405)
            self._send_post('/v1/users/1/relationship/geokrety-held', code=405, user=self.admin)
            self._send_post('/v1/users/1/relationship/geokrety-held', code=405, user=self.user1)
            self._send_post('/v1/users/1/relationship/geokrety-held', code=405, user=self.user2)

    def test_patch_geokrety_held_status_codes(self):
        """Check GeokretRelationships: PATCH geokrety-held - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_patch('/v1/users/1/relationship/geokrety-held', code=405)
            self._send_patch('/v1/users/1/relationship/geokrety-held', code=405, user=self.admin)
            self._send_patch('/v1/users/1/relationship/geokrety-held', code=405, user=self.user1)
            self._send_patch('/v1/users/1/relationship/geokrety-held', code=405, user=self.user2)

    def test_delete_geokrety_held_status_codes(self):
        """Check GeokretRelationships: DELETE geokrety-held - status codes"""
        with app.test_request_context():
            self._blend_users()
            self._send_delete('/v1/users/1/relationship/geokrety-held', code=405)
            self._send_delete('/v1/users/1/relationship/geokrety-held', code=405, user=self.admin)
            self._send_delete('/v1/users/1/relationship/geokrety-held', code=405, user=self.user1)
            self._send_delete('/v1/users/1/relationship/geokrety-held', code=405, user=self.user2)
