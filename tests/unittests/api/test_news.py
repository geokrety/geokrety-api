from app import current_app as app
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestNews(GeokretyTestCase):
    """Test News CRUD operations"""

    # def setUp(self):
    #     super(TestNews, self).setUp()
    #     with app.test_request_context():
    #         self._blend_users()

    def _blend_users(self):
        """Create mocked User/News/NewsComments"""
        mixer.init_app(app)
        self.admin = mixer.blend(User)
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)

    def _blend(self):
        """Create mocked User/News/NewsComments"""
        self.news1 = mixer.blend(News, author=self.user1)
        # self.news2 = mixer.blend(News)
        self.orphan_news = mixer.blend(News, author=None)
        self.newscomment1 = mixer.blend(NewsComment, author=self.user1, news=self.news1)
        # self.newscomment2 = mixer.blend(NewsComment, author=self.user2, news=self.news1)

    def _check_news_details(self, data, news):
        self.assertTrue('attributes' in data['data'])
        attributes = data['data']['attributes']
        relationships = data['data']['relationships']

        self.assertTrue('title' in attributes)
        self.assertTrue('content' in attributes)
        # self.assertTrue('username' in attributes)

        self.assertEqual(attributes['title'], news.title)
        self.assertEqual(attributes['content'], news.content)
        if 'username' in attributes:
            self.assertEqual(attributes['username'], news.username)

        self.assertEqual('author' in relationships, hasattr(news, 'author'))
        self.assertTrue('links' in relationships['author'])
        self.assertTrue('self' in relationships['author']['links'])
        self.assertTrue('related' in relationships['author']['links'])

        self.assertEqual('news' in relationships, hasattr(news, 'news-comments'))
        self.assertTrue('links' in relationships['news-comments'])
        self.assertTrue('self' in relationships['news-comments']['links'])
        self.assertTrue('related' in relationships['news-comments']['links'])

    def _check_news_list(self, data, length):
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), length)

        for news in data['data']:
            self.assertTrue('attributes' in news)
            attributes = news['attributes']

            self.assertTrue('title' in attributes)
            self.assertTrue('content' in attributes)
            self.assertTrue('username' in attributes)

    def _post_news(self, payload, code=201, expected_count=1, user=None):
        """Check News: POST request minimal informations"""
        with app.test_request_context():
            response = self._send_post("/v1/news", payload=payload, code=code, user=user)
            self.assertEqual(len(News.query.all()), expected_count)
            return response

    def test_post_content_types(self):
        """Check News: POST accepted content types"""
        with app.test_request_context():
            self._blend_users()
            self._send_post("/v1/news", payload="not a json", code=415,
                            content_type='application/json', user=self.admin)
            self._send_post("/v1/news", payload={}, code=422, user=self.admin)
            self._send_post("/v1/news", payload={"user": "kumy"}, code=422, user=self.admin)

    def test_create_incomplete_1(self):
        """Check News: POST request incomplete 1"""
        payload = {
            "data": {
                "type": "news"
            }
        }
        with app.test_request_context():
            self._blend_users()
            self._post_news(payload, code=422, expected_count=0, user=self.admin)

    def test_create_incomplete_2(self):
        """Check News: POST request incomplete 2"""
        payload = {
            "data": {
                "type": "news",
                "attributes": {
                    "title": "News title"
                }
            }
        }
        with app.test_request_context():
            self._blend_users()
            self._post_news(payload, code=422, expected_count=0, user=self.admin)

    def test_create_incomplete_3(self):
        """Check News: POST request incomplete 3"""
        payload = {
            "data": {
                "type": "news",
                "attributes": {
                    "content": "News content"
                }
            }
        }
        with app.test_request_context():
            self._blend_users()
            self._post_news(payload, code=422, expected_count=0, user=self.admin)

    def test_create_minimal(self):
        """Check News: POST request minimal informations"""
        payload = {
            "data": {
                "type": "news",
                "attributes": {
                    "title": "News title",
                    "content": "News content"
                }
            }
        }
        with app.test_request_context():
            self._blend_users()
            self._post_news(payload, code=401, expected_count=0)
            self._post_news(payload, code=201, expected_count=1, user=self.admin)
            self._post_news(payload, code=403, expected_count=1, user=self.user1)
            self._post_news(payload, code=403, expected_count=1, user=self.user2)

    def test_create_with_username(self):
        """Check News: POST request with username"""
        payload = {
            "data": {
                "type": "news",
                "attributes": {
                    "title": "News title",
                    "content": "News content",
                    "username": "someone"
                }
            }
        }
        with app.test_request_context():
            self._blend_users()
            self._post_news(payload, code=401, expected_count=0)
            self._post_news(payload, code=201, expected_count=1, user=self.admin)
            self._post_news(payload, code=403, expected_count=1, user=self.user1)
            self._post_news(payload, code=403, expected_count=1, user=self.user2)

    def test_create_with_author(self):
        """Check News: POST request with author"""
        with app.test_request_context():
            self._blend_users()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "title": "News title",
                        "content": "News content"
                    },
                    "relationships": {
                        "author": {
                            "data": {
                                "type": "user",
                                "id": self.admin.id
                            }
                        }
                    }
                }
            }

            self._post_news(payload, code=401, expected_count=0)
            self._post_news(payload, code=201, expected_count=1, user=self.admin)
            self._post_news(payload, code=403, expected_count=1, user=self.user1)
            self._post_news(payload, code=403, expected_count=1, user=self.user2)

    def test_create_full(self):
        """Check News: POST request full"""
        with app.test_request_context():
            self._blend_users()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "title": "News title",
                        "content": "News content",
                        "username": "someone"
                    },
                    "relationships": {
                        "author": {
                            "data": {
                                "type": "user",
                                "id": self.admin.id
                            }
                        }
                    }
                }
            }
            self._post_news(payload, code=401, expected_count=0)
            self._post_news(payload, code=201, expected_count=1, user=self.admin)
            self._post_news(payload, code=403, expected_count=1, user=self.user1)
            self._post_news(payload, code=403, expected_count=1, user=self.user2)

    def test_get_list(self):
        """Check News: GET news listing"""
        with app.test_request_context():
            self._blend_users()
            self._blend()

            response = self._send_get('/v1/news', code=200)
            self._check_news_list(response, length=2)

            response = self._send_get('/v1/news', code=200, user=self.admin)
            self._check_news_list(response, length=2)

            response = self._send_get('/v1/news', code=200, user=self.user1)
            self._check_news_list(response, length=2)

            response = self._send_get('/v1/news', code=200, user=self.user2)
            self._check_news_list(response, length=2)

    def test_get_list_from_user(self):
        """Check News: GET news listing from user"""
        with app.test_request_context():
            self._blend_users()
            self._blend()

            response = self._send_get('/v1/users/%s/news' % self.news1.author.id, code=200)
            self._check_news_list(response, length=1)

            response = self._send_get('/v1/users/%s/news' % self.news1.author.id, code=200, user=self.admin)
            self._check_news_list(response, length=1)

            response = self._send_get('/v1/users/%s/news' % self.news1.author.id, code=200, user=self.user1)
            self._check_news_list(response, length=1)

            response = self._send_get('/v1/users/%s/news' % self.news1.author.id, code=200, user=self.user2)
            self._check_news_list(response, length=1)

            response = self._send_get('/v1/users/666/news', code=404, user=self.admin)

            response = self._send_get('/v1/users/%s/news' % self.admin.id, code=200, user=self.admin)
            self._check_news_list(response, length=0)
            response = self._send_get('/v1/users/%s/news' % self.user2.id, code=200, user=self.admin)
            self._check_news_list(response, length=0)

    def test_get_details(self):
        """Check News: GET news details"""
        with app.test_request_context():
            self._blend_users()
            self._blend()

            response = self._send_get('/v1/news/%s' % self.news1.id, code=200)
            self._check_news_details(response, self.news1)

            response = self._send_get('/v1/news/%s' % self.news1.id, code=200, user=self.admin)
            self._check_news_details(response, self.news1)

            response = self._send_get('/v1/news/%s' % self.news1.id, code=200, user=self.user1)
            self._check_news_details(response, self.news1)

            response = self._send_get('/v1/news/%s' % self.news1.id, code=200, user=self.user2)
            self._check_news_details(response, self.news1)

            response = self._send_get('/v1/news/666', code=404, user=self.admin)

    def test_get_details_from_news_comment(self):
        """Check News: GET news details from news comment"""
        with app.test_request_context():
            self._blend_users()
            self._blend()

            response = self._send_get('/v1/news-comments/%s/news' % self.newscomment1.id, code=200)
            self._check_news_details(response, self.newscomment1.news)

            response = self._send_get('/v1/news-comments/%s/news' % self.newscomment1.id, code=200, user=self.admin)
            self._check_news_details(response, self.newscomment1.news)

            response = self._send_get('/v1/news-comments/%s/news' % self.newscomment1.id, code=200, user=self.user1)
            self._check_news_details(response, self.newscomment1.news)

            response = self._send_get('/v1/news-comments/%s/news' % self.newscomment1.id, code=200, user=self.user2)
            self._check_news_details(response, self.newscomment1.news)

            response = self._send_get('/v1/news-comments/666/news', code=404, user=self.admin)

    def test_patch_list(self):
        """
        Check News: PATCH list cannot be patched
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_patch("/v1/news", code=405)
            self._send_patch("/v1/news", code=405, user=self.admin)
            self._send_patch("/v1/news", code=405, user=self.user1)
            self._send_patch("/v1/news", code=405, user=self.user2)

    def test_patch_title(self):
        """
        Check News: PATCH title
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "title": "Fresh News title"
                    }
                }
            }

            payload["data"]["id"] = "1"
            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/news/2", payload=payload, code=404)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.admin)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user1)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user2)

    def test_patch_content(self):
        """
        Check News: PATCH content
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "content": "Fresh News content"
                    }
                }
            }

            payload["data"]["id"] = "1"
            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/news/2", payload=payload, code=404)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.admin)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user1)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user2)

    def test_patch_username(self):
        """
        Check News: PATCH username
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "username": ""
                    }
                }
            }

            payload["data"]["id"] = "1"
            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/news/2", payload=payload, code=404)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.admin)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user1)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user2)

    def test_patch_full(self):
        """
        Check News: PATCH full
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "type": "news",
                    "attributes": {
                        "title": "Fresh News title",
                        "content": "Fresh News content",
                        "username": ""
                    }
                }
            }

            payload["data"]["id"] = "1"
            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/news/2", payload=payload, code=404)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.admin)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user1)
            self._send_patch("/v1/news/2", payload=payload, code=404, user=self.user2)

    def test_patch_nothing(self):
        """
        Check News: PATCH nothing
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "id": "1",
                    "type": "news",
                    "attributes": {
                    }
                }
            }

            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

    def test_patch_same_data(self):
        """
        Check News: PATCH same data
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            payload = {
                "data": {
                    "id": "1",
                    "type": "news",
                    "attributes": {
                        "title": self.news1.title,
                        "content": self.news1.content
                    }
                }
            }

            self._send_patch("/v1/news/1", payload=payload, code=401)
            self._send_patch("/v1/news/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news/1", payload=payload, code=403, user=self.user2)

    def test_delete_list(self):
        """
        Check News: DELETE list
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_delete("/v1/news", code=405)
            self._send_delete("/v1/news", code=405, user=self.admin)
            self._send_delete("/v1/news", code=405, user=self.user1)
            self._send_delete("/v1/news", code=405, user=self.user2)

    def test_delete_anonymous(self):
        """
        Check News: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_delete("/v1/news/1", code=401)
            self._send_delete("/v1/news/2", code=404)

    def test_delete_admin(self):
        """
        Check News: DELETE Admin
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_delete("/v1/news/1", code=200, user=self.admin)
            self._send_delete("/v1/news/2", code=404, user=self.admin)

    def test_delete_user1(self):
        """
        Check News: DELETE User1
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_delete("/v1/news/1", code=403, user=self.user1)
            self._send_delete("/v1/news/2", code=404, user=self.user1)

    def test_delete_user2(self):
        """
        Check News: DELETE User2
        """
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_delete("/v1/news/1", code=403, user=self.user2)
            self._send_delete("/v1/news/2", code=404, user=self.user2)
