import json

from app import current_app as app
from tests.unittests.utils import GeokretyTestCase

from app.models import db
from app.factories.news import NewsFactory
from app.factories.news_comment import NewsCommentFactory
from app.factories.user import UserFactory


class TestUser(GeokretyTestCase):

    def test_post_content_types(self):
        """
        Check accepted content types
        """

        self._send_post("/v1/users", "not a json", 415, content_type='application/json')  # Bad content_type
        # self._send_post("/v1/users", "not a json", 400)  # Bad body
        self._send_post("/v1/users", {}, 422)  # Bad body
        self._send_post("/v1/users", {"user": "kumy"}, 422)  # Bad body

    def test_create_incomplete(self):
        """
        Check incomplete create request
        """

        payload = {
            "data": {
                "type": "user"
            }
        }
        self._send_post("/v1/users", payload, 500)

    def test_create(self):
        """
        Check complete create request
        """

        payload = {
            "data": {
                "type": "user",
                    "attributes": {
                        "name": "kumy",
                        "password": "password",
                        "email": "email@email.email"
                    }
            }
        }
        self._send_post("/v1/users", payload, 201)

    def test_list_authenticated(self):
        """
        Check GET user listing must be authenticated
        """

        # Unauthenticated
        self._send_get('/v1/users', code=401, auth=False)
        self._send_get('/v1/users', code=200, auth=True, create=True)

    def test_create_user(self):
        """
        Check create and Read back an user
        """

        with app.test_request_context():
            # Test inserting first user
            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                        "name": "kumy",
                        "password": "password",
                        "email": "kumy@email.email"
                    }
                }
            }
            self._send_post("/v1/users", payload, 201)

            # authenticate with fresh user
            self._login("kumy", "password")

            # read user list
            response = self._send_get('/v1/users', code=200, auth=True)
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
                        "name": "filips",
                        "password": "password",
                        "email": "filips@email.email"
                    }
                }
            }
            self._send_post("/v1/users", payload, 201)

            # read it back
            response = self._send_get('/v1/users', code=200, auth=True)

            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data['data']), 2)
            self.assertTrue('attributes' in data['data'][1])
            self.assertTrue('name' in data['data'][1]['attributes'])
            self.assertEqual(data['data'][1]['attributes']['name'], "filips")

    def test_get_news_no_author(self):
        """
        Check GET author from a news, no author
        """

        with app.test_request_context():
            news = NewsFactory()
            db.session.add(news)
            db.session.commit()
            self._send_get('/v1/news/1/author', code=404, auth=True, create=True)

    def test_get_news_author(self):
        """
        Check GET author from a news
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            db.session.commit()

            self._send_get('/v1/news/1/author', code=200, auth=True, user=user.name)

    def test_get_news_comment_author(self):
        """
        Check GET author from a news_comment
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

            self._send_get('/v1/news-comments/1/author', code=200, auth=True, user=user.name)
