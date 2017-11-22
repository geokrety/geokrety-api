from app import current_app as app
from app.api.helpers.jwt import get_identity, jwt_authenticate
from app.models.user import User
from flask_jwt import _default_jwt_encode_handler
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestJWTHelperValidation(GeokretyTestCase):

    def test_jwt_authenticate(self):
        """Check JWTHelper: authenticate"""
        with app.test_request_context():
            mixer.init_app(app)
            user = mixer.blend(User)

            # Valid Authentication
            authenticated_user = jwt_authenticate(user.name, user.password)
            self.assertEqual(authenticated_user.name, user.name)

            # Invalid Authentication
            wrong_credential_user = jwt_authenticate(user.name, 'wrong_password')
            self.assertIsNone(wrong_credential_user)

    def test_get_identity(self):
        """Check JWTHelper: get user identity"""
        with app.test_request_context():
            mixer.init_app(app)
            user = mixer.blend(User)

            # Authenticate User
            self.auth = {'Authorization': "JWT " + _default_jwt_encode_handler(user)}

        with app.test_request_context(headers=self.auth):
            self.assertEquals(get_identity().id, user.id)
