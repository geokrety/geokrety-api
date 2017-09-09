from app import current_app as app
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.schema.users import UserSchema
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestUser(GeokretyTestCase):
    """Test User CRUD operations"""

    def test_user_name_uniqueness(self):
        """User name uniqueness - Check run without exception"""
        with app.test_request_context():
            UserSchema.validate_username_uniqueness(UserSchema(), "someone")

    def test_user_name_uniqueness_taken(self):
        """User name uniqueness - Detect username already taken"""
        with app.test_request_context():
            with self.assertRaises(UnprocessableEntity):
                mixer.init_app(app)
                mixer.blend(User, name="someone")
                UserSchema.validate_username_uniqueness(UserSchema(), "someone")

    def test_validate_email_uniqueness(self):
        """User email uniqueness - Check run without exception"""
        with app.test_request_context():
            UserSchema.validate_email_uniqueness(UserSchema(), "someone@email.email")

    def test_validate_email_uniqueness_taken(self):
        """User email uniqueness - Detect email already taken"""
        with app.test_request_context():
            with self.assertRaises(UnprocessableEntity):
                mixer.init_app(app)
                mixer.blend(User, email="someone@email.email")
                UserSchema.validate_email_uniqueness(UserSchema(), "someone@email.email")
