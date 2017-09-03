import json

from app import current_app as app
from tests.unittests.utils import GeokretyTestCase

from app.models import db
from app.factories.news import NewsFactory
from app.factories.news_comment import NewsCommentFactory
from app.factories.user import UserFactory


class TestNewsComment(GeokretyTestCase):

    def test_post_content_types(self):
        """
        Check accepted content types
        """

        with app.test_request_context():
            user = UserFactory(name="kumy")
            db.session.add(user)
            db.session.commit()

        self._send_post("/v1/news-comments", "not a json", 415, content_type='application/json', auth=True, user="kumy")  # Bad content_type
        # self._send_post("/v1/users", "not a json", 400)  # Bad body
        self._send_post("/v1/news-comments", {}, 422, auth=True, user="kumy")  # Bad body
        self._send_post("/v1/news-comments", {"user": "kumy"}, 422, auth=True, user="kumy")  # Bad body

    def test_create_incomplete(self):
        """
        Check incomplete create request
        """

        with app.test_request_context():
            user = UserFactory(name="kumy")
            db.session.add(user)
            db.session.commit()

        payload = {
            "data": {
                "type": "news-comment"
            }
        }
        self._send_post("/v1/news-comments", payload, 500, auth=True, user="kumy")

    def test_create(self):
        """
        Check complete create request
        """

        with app.test_request_context():
            user = UserFactory(name="kumy")
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            db.session.commit()

        payload = {
            "data": {
                "type": "news-comment",
                    "attributes": {
                        "comment": "News comment",
                        "news_id": 1,
                        "author_id": 1
                    }
            }
        }
        self._send_post("/v1/news-comments", payload, 401)
        self._send_post("/v1/news-comments", payload, 201, auth=True)

    def test_create_from_news(self):
        """
        Check complete create request from news comment
        """

        with app.test_request_context():
            user = UserFactory(name="kumy")
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            db.session.commit()

        payload = {
            "data": {
                "type": "news-comment",
                    "attributes": {
                        "comment": "News comment",
                        "author_id": 1
                    }
            }
        }
        self._send_post("/v1/news/1/news-comments", payload, 401)
        self._send_post("/v1/news/2/news-comments", payload, 401)
        self._send_post("/v1/news/1/news-comments", payload, 201, auth=True)
        self._send_post("/v1/news/2/news-comments", payload, 404, auth=True)

    def test_list_public(self):
        """
        Check GET news-comments listing is public
        """

        # Unauthenticated
        self._send_get('/v1/news-comments', code=200, auth=False)
        self._send_get('/v1/news-comments', code=200, auth=True, create=True)

    def test_list_comments_from_news(self):
        """
        Check GET news-comments listing from news
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

        # Unauthenticated
        response = self._send_get('/v1/news/1/news-comments', code=200, auth=False)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['data']), 1)
        self.assertTrue('attributes' in data['data'][0])
        self.assertTrue('comment' in data['data'][0]['attributes'])
        self.assertEqual(data['data'][0]['attributes']['comment'], "News comment text")
        self.assertEqual(data['data'][0]['relationships']['author']['links']['related'], u'/v1/users/1')
        self.assertEqual(data['data'][0]['relationships']['news']['links']['related'], u'/v1/news/1')

        self._send_get('/v1/news/1/news-comments', code=200, auth=True, create=True)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['data']), 1)
        self.assertTrue('attributes' in data['data'][0])
        self.assertTrue('comment' in data['data'][0]['attributes'])
        self.assertEqual(data['data'][0]['attributes']['comment'], "News comment text")
        self.assertEqual(data['data'][0]['relationships']['author']['links']['related'], u'/v1/users/1')
        self.assertEqual(data['data'][0]['relationships']['news']['links']['related'], u'/v1/news/1')

    def test_details_public(self):
        """
        Check GET news-comments details is public
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

        # Unauthenticated
        self._send_get('/v1/news-comments/1', code=200, auth=True, create=True)
        self._send_get('/v1/news-comments/1', code=200, auth=False)
        self._send_get('/v1/news-comments/2', code=404, auth=False)
        self._send_get('/v1/news/1/news-comments', code=200, auth=True)
        self._send_get('/v1/news/1/news-comments', code=200, auth=False)
        self._send_get('/v1/news/2/news-comments', code=404, auth=False)

    def test_news_comment_details(self):
        """
        Check GET news-comments details
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)
            news = NewsFactory(author=user)
            db.session.add(news)
            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

            # read user list
            response = self._send_get('/v1/news-comments/1', code=200)
            data = json.loads(response.get_data(as_text=True))
            self.assertTrue('attributes' in data['data'])
            self.assertTrue('comment' in data['data']['attributes'])
            self.assertEqual(data['data']['attributes']['comment'], newscomment.comment)
            self.assertEqual(data['data']['relationships']['author']['links']['related'], u'/v1/users/1')
            self.assertEqual(data['data']['relationships']['news']['links']['related'], u'/v1/news/1')

    def test_create_news_comment(self):
        """
        Check create and Read back a news_comment
        """

        with app.test_request_context():
            user1 = UserFactory()
            db.session.add(user1)
            news1 = NewsFactory(author=user1)
            db.session.add(news1)

            user2 = UserFactory()
            db.session.add(user2)
            news2 = NewsFactory(author=user2)
            db.session.add(news2)
            db.session.commit()

            # Test inserting first user
            payload = {
                "data": {
                    "type": "news-comment",
                        "attributes": {
                            "comment": "News comment 1",
                            "news_id": 1,
                            "author_id": 1
                        }
                }
            }
            self._login(user1.name, "password")
            self._send_post("/v1/news-comments", payload, 201, auth=True, user=user1.name)

            # read user list
            response = self._send_get('/v1/news-comments', code=200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data['data']), 1)
            self.assertTrue('attributes' in data['data'][0])
            self.assertTrue('comment' in data['data'][0]['attributes'])
            self.assertEqual(data['data'][0]['attributes']['comment'], "News comment 1")
            self.assertEqual(data['data'][0]['relationships']['author']['links']['related'], u'/v1/users/1')
            self.assertEqual(data['data'][0]['relationships']['news']['links']['related'], u'/v1/news/1')

            # Test inserting a second user
            payload = {
                "data": {
                    "type": "news-comment",
                        "attributes": {
                            "comment": "News comment 2",
                            "news_id": 2,
                            "author_id": 2
                        }
                }
            }
            self._send_post("/v1/news-comments", payload, 201, auth=True, user=user1.name)

            # read it back
            response = self._send_get('/v1/news-comments', code=200, auth=True, user=user1.name)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data['data']), 2)
            self.assertTrue('attributes' in data['data'][1])
            self.assertTrue('comment' in data['data'][1]['attributes'])
            self.assertEqual(data['data'][1]['attributes']['comment'], "News comment 2")
            self.assertEqual(data['data'][1]['relationships']['author']['links']['related'], u'/v1/users/2')
            self.assertEqual(data['data'][1]['relationships']['news']['links']['related'], u'/v1/news/2')

    # def test_get_news_comment_author(self):
    #     """
    #     Check GET author from a news_comment
    #     """
    #
    #     with app.test_request_context():
    #         user = UserFactory()
    #         db.session.add(user)
    #         news = NewsFactory(author=user)
    #         db.session.add(news)
    #         newscomment = NewsCommentFactory(author=user, news=news)
    #         db.session.add(newscomment)
    #         db.session.commit()
    #
    #         self._send_get('/v1/news-comments/1/author', code=200, auth=True, user=user.name)
