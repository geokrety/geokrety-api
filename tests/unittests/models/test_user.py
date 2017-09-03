from sqlalchemy.exc import IntegrityError, OperationalError

from tests.unittests.utils import GeokretyTestCase
from app.models.user import User
from app.models import db
from app import current_app as app
from app.factories.user import UserFactory


class TestUser(GeokretyTestCase):

    def test_lookup(self):
        """
        Check create user and read back
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            db.session.commit()
            users = User.query.all()
            self.assertTrue(user in users)
            self.assertEqual(len(users), 1)

    def test_mandatory_fields(self):
        """
        Check User mandatory fields
        """

        with app.test_request_context():
            user = User()
            self._check_commit_and_raise(user, OperationalError)
            user.name = "kumy"
            self._check_commit_and_raise(user, OperationalError)
            user.password = "password"
            self._check_commit_and_raise(user, OperationalError)
            user.email = "email@email.email"
            self._check_commit_and_not_raise(user)


    def test_duplicate_username(self):
        """
        Check create duplicated username
        """

        with app.test_request_context():
            user = UserFactory(name="kumy", email="email1@email.email")
            db.session.add(user)
            db.session.commit()

            user2 = UserFactory(name="kumy", email="email2@email.email")
            db.session.add(user2)
            with self.assertRaises(IntegrityError):
                db.session.commit()
            db.session.rollback()


    def test_duplicate_email(self):
        """
        Check create duplicated email
        """

        with app.test_request_context():
            user = UserFactory(name="kumy", email="email1@email.email")
            db.session.add(user)
            db.session.commit()

            user2 = UserFactory(name="kumy2", email="email2@email.email")
            db.session.add(user2)
            self._check_commit_and_not_raise(user2)


    def test_function_get_id(self):
        """
        Check function get_id()
        """

        with app.test_request_context():
            user = UserFactory()
            self.assertEqual(user.get_id(), None)

            db.session.add(user)
            db.session.commit()
            self.assertEqual(user.get_id(), 1)


    def test_function_is_active(self):
        """
        Check function is_active()
        """

        with app.test_request_context():
            user = UserFactory()
            self.assertTrue(user.is_active())


    def test_function_is_authenticated(self):
        """
        Check function is_authenticated()
        """

        with app.test_request_context():
            user = UserFactory()
            self.assertTrue(user.is_authenticated())


    def test_function_is_super_admin(self):
        """
        Check function is_super_admin()
        """

        with app.test_request_context():
            user = UserFactory(id=1)
            self.assertTrue(user.is_super_admin)

            user = UserFactory(id=2)
            self.assertFalse(user.is_super_admin)


    def test_function_is_admin(self):
        """
        Check function is_admin()
        """

        with app.test_request_context():
            user = UserFactory(id=1)
            self.assertTrue(user.is_admin)

            user = UserFactory(id=2)
            self.assertFalse(user.is_admin)
