from app import current_app as app
from tests.unittests.utils import GeokretyTestCase
from app.api.helpers.db import save_to_db, safe_query, get_or_create, get_count
from flask_rest_jsonapi.exceptions import ObjectNotFound
from app.models import db
from app.models.user import User
from app.factories.user import UserFactory
from tests.unittests.setup_database import Setup


class TestDBHelperValidation(GeokretyTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_save_to_db(self):
        with app.test_request_context():
            obj = UserFactory()
            save_to_db(obj)
            user = db.session.query(User).filter(User.id == obj.id).first()
            self.assertEqual(obj.name, user.name)

    def test_safe_query(self):
        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            db.session.commit()
            obj = safe_query(db, User, 'id', user.id, 'user_id')
            self.assertEqual(obj.name, user.name)

    def test_safe_query_exception(self):
        with app.test_request_context():
            self.assertRaises(ObjectNotFound, lambda: safe_query(db, User, 'id', 1, 'user_id'))

    def test_get_or_create(self):
        with app.test_request_context():
            user = UserFactory()
            save_to_db(user)
            obj, is_created = get_or_create(User, name=user.name)
            self.assertEqual(user.id, obj.id)
            self.assertFalse(is_created)

            obj, is_created = get_or_create(User, name="new user")
            self.assertNotEqual(user.id, obj.id)
            self.assertTrue(is_created)

    def test_get_count(self):
        with app.test_request_context():
            user = UserFactory()
            save_to_db(user)
            self.assertEqual(get_count(User.query), 1)
