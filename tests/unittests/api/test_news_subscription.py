from app import current_app as app
from app.models import db
from app.models.news import News
from app.models.news_subscription import NewsSubscription
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestNewsSubscription(GeokretyTestCase):
    """Test News Subscription CRUD operations"""

    def _blend_subscription(self):
        """Create mocked News Subscriptions"""
        mixer.init_app(app)
        self.subscription1 = mixer.blend(NewsSubscription, user=self.admin, news=self.news1)
        self.subscription2 = mixer.blend(NewsSubscription, user=self.user1, news=self.news1)

    def _blend(self):
        """Create mocked User/News/NewsComments"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            self.news1 = mixer.blend(News, author=self.user1)
            self.news2 = mixer.blend(News)
            self.orphan_news = mixer.blend(News, author=None)
            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.add(self.news1)
            db.session.add(self.news2)
            db.session.add(self.orphan_news)
            db.session.commit()

    def _check_news_subscription_details(self, data, news):
        pass
        # import pprint
        # pprint.pprint(data)
        # print(news.id, news.title, news.content)
        # self.assertTrue('attributes' in data['data'])
        # attributes = data['data']['attributes']
        #
        # self.assertTrue('title' in attributes)
        # self.assertTrue('content' in attributes)
        # self.assertTrue('username' in attributes)
        #
        # self.assertEqual(attributes['title'], news.title)
        # self.assertEqual(attributes['content'], news.content)
        # self.assertEqual(attributes['username'], news.username)

    def _check_news_subscription_list(self, data, length):
        pass
        # self.assertTrue('data' in data)
        # self.assertEqual(len(data['data']), length)
        #
        # for news in data['data']:
        #     self.assertTrue('attributes' in news)
        #     attributes = news['attributes']
        #
        #     self.assertTrue('title' in attributes)
        #     self.assertTrue('content' in attributes)
        #     self.assertTrue('username' in attributes)

    def _subscribe(self, payload, code=201, expected_count=1, user=None):
        """Check NewsSubscription: POST request minimal informations"""
        with app.test_request_context():
            self._send_post("/v1/news-subscriptions", payload=payload, code=code, user=user)
            self.assertEqual(len(NewsSubscription.query.all()), expected_count)

    def test_post_content_types(self):
        """Check NewsSubscription: POST accepted content types"""
        with app.test_request_context():
            self._blend()
            self._send_post("/v1/news-subscriptions", payload="not a json", code=415,
                            content_type='application/json', user=self.admin)
            self._send_post("/v1/news-subscriptions", payload={}, code=422, user=self.admin)
            self._send_post("/v1/news-subscriptions", payload={"subscribed": True}, code=422, user=self.admin)

    def test_subscribe_incomplete_1(self):
        """Check NewsSubscription: POST request incomplete 1"""
        payload = {
            "data": {
                "type": "news-subscription"
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=422, expected_count=0, user=self.admin)

    def test_subscribe_incomplete_2(self):
        """Check NewsSubscription: POST request incomplete 2"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": True
                }
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=422, expected_count=0, user=self.admin)

    def test_subscribe_incomplete_3(self):
        """Check NewsSubscription: POST request incomplete 3"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": True
                }
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=422, expected_count=0, user=self.admin)

    def test_subscribe_implicit_user(self):
        """Check NewsSubscription: POST request minimal informations"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": True
                },
                "relationships": {
                    "news": {
                        "data": {
                            "type": "news",
                            "id": "1"
                        }
                    }
                }
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=401, expected_count=0)
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)
            self._subscribe(payload, code=201, expected_count=2, user=self.user1)
            self._subscribe(payload, code=201, expected_count=3, user=self.user2)

    def test_subscribe_with_user(self):
        """Check NewsSubscription: POST subscribe with user"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": True
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "user",
                            "id": None
                        }
                    },
                    "news": {
                        "data": {
                            "type": "news",
                            "id": 1
                        }
                    }
                }
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=401, expected_count=0)

            payload['data']['relationships']['user']['data']['id'] = self.admin.id
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)

            payload['data']['relationships']['user']['data']['id'] = self.user1.id
            self._subscribe(payload, code=201, expected_count=2, user=self.user1)

            payload['data']['relationships']['user']['data']['id'] = self.user2.id
            self._subscribe(payload, code=201, expected_count=3, user=self.user2)

    def test_subscribe_someone_else(self):
        """Check NewsSubscription: POST subscribe someone else"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": True
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "user",
                            "id": None
                        }
                    },
                    "news": {
                        "data": {
                            "type": "news",
                            "id": 1
                        }
                    },
                }
            }
        }
        with app.test_request_context():
            self._blend()
            self._subscribe(payload, code=401, expected_count=0)

            payload['data']['relationships']['user']['data']['id'] = self.user2.id
            self._subscribe(payload, code=403, expected_count=0, user=self.user1)

            payload['data']['relationships']['user']['data']['id'] = self.user1.id
            self._subscribe(payload, code=403, expected_count=0, user=self.user2)

            payload['data']['relationships']['user']['data']['id'] = self.user1.id
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)

            payload['data']['relationships']['user']['data']['id'] = self.user2.id
            self._subscribe(payload, code=201, expected_count=2, user=self.admin)

    def test_unsubscribe(self):
        """Check NewsSubscription: POST with subscribed=false autodelete rows"""
        payload = {
            "data": {
                "type": "news-subscription",
                "attributes": {
                    "subscribed": None
                },
                "relationships": {
                    "news": {
                        "data": {
                            "type": "news",
                            "id": "1"
                        }
                    }
                }
            }
        }
        with app.test_request_context():
            self._blend()
            payload["data"]["attributes"]["subscribed"] = False
            self._subscribe(payload, code=201, expected_count=0, user=self.admin)

            payload["data"]["attributes"]["subscribed"] = True
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)

            payload["data"]["attributes"]["subscribed"] = False
            payload["data"]["relationships"]["news"]["data"]["id"] = 2
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)

            payload["data"]["attributes"]["subscribed"] = True
            payload["data"]["relationships"]["news"]["data"]["id"] = 2
            self._subscribe(payload, code=201, expected_count=2, user=self.admin)

            payload["data"]["attributes"]["subscribed"] = False
            payload["data"]["relationships"]["news"]["data"]["id"] = 1
            self._subscribe(payload, code=201, expected_count=1, user=self.admin)

            payload["data"]["attributes"]["subscribed"] = False
            payload["data"]["relationships"]["news"]["data"]["id"] = 2
            self._subscribe(payload, code=201, expected_count=0, user=self.admin)

    def test_get_list(self):
        """Check NewsSubscription: GET news-subscriptions listing"""
        with app.test_request_context():
            self._blend()
            self._blend_subscription()

            response = self._send_get("/v1/news-subscriptions", code=401)

            response = self._send_get("/v1/news-subscriptions", code=200, user=self.admin)
            self._check_news_subscription_list(response, length=2)

            response = self._send_get("/v1/news-subscriptions", code=200, user=self.user1)
            self._check_news_subscription_list(response, length=1)

            response = self._send_get("/v1/news-subscriptions", code=200, user=self.user2)
            self._check_news_subscription_list(response, length=0)

    def test_get_list_from_user(self):
        """Check NewsSubscription: GET news-subscriptions listing from user"""
        with app.test_request_context():
            self._blend()
            self._blend_subscription()

            self._send_get("/v1/users/%s/news-subscriptions" % self.user1.id, code=401)

            response = self._send_get("/v1/users/%s/news-subscriptions" % self.user1.id, code=200, user=self.admin)
            self._check_news_subscription_list(response, length=1)

            response = self._send_get("/v1/users/%s/news-subscriptions" % self.user1.id, code=200, user=self.user1)
            self._check_news_subscription_list(response, length=1)

            self._send_get("/v1/users/%s/news-subscriptions" % self.user1.id, code=403, user=self.user2)

            response = self._send_get('/v1/users/666/news-subscriptions', code=404, user=self.admin)

            response = self._send_get("/v1/users/%s/news-subscriptions" % self.user2.id, code=200, user=self.admin)
            self._check_news_subscription_list(response, length=0)

            self._send_get("/v1/users/%s/news-subscriptions" % self.user2.id, code=403, user=self.user1)

            response = self._send_get("/v1/users/%s/news-subscriptions" % self.user2.id, code=200, user=self.user2)
            self._check_news_subscription_list(response, length=0)

    def test_get_list_from_news(self):
        """Check NewsSubscription: GET news-subscriptions listing from news"""
        with app.test_request_context():
            self._blend()
            self._blend_subscription()

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news1.id, code=401)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news1.id, code=200, user=self.admin)
            self._check_news_subscription_list(response, length=2)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news1.id, code=200, user=self.user1)
            self._check_news_subscription_list(response, length=1)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news1.id, code=200, user=self.user2)
            self._check_news_subscription_list(response, length=0)

            response = self._send_get('/v1/news/666/news-subscriptions', code=404, user=self.admin)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news2.id, code=200, user=self.admin)
            self._check_news_subscription_list(response, length=0)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news2.id, code=200, user=self.user1)
            self._check_news_subscription_list(response, length=0)

            response = self._send_get("/v1/news/%s/news-subscriptions" % self.news2.id, code=200, user=self.user2)
            self._check_news_subscription_list(response, length=0)

    def test_get_details(self):
        """Check NewsSubscription: GET news-subscriptions details"""
        with app.test_request_context():
            self._blend()
            self._blend_subscription()

            self._send_get("/v1/news-subscriptions/%s" % self.subscription1.id, code=401)

            response = self._send_get("/v1/news-subscriptions/%s" % self.subscription1.id, code=200, user=self.admin)
            self._check_news_subscription_details(response, self.subscription1)

            response = self._send_get("/v1/news-subscriptions/%s" % self.subscription2.id, code=200, user=self.admin)
            self._check_news_subscription_details(response, self.subscription2)

            self._send_get("/v1/news-subscriptions/%s" % self.subscription1.id, code=403, user=self.user1)

            response = self._send_get("/v1/news-subscriptions/%s" % self.subscription2.id, code=200, user=self.user1)
            self._check_news_subscription_details(response, self.subscription2)

            self._send_get("/v1/news-subscriptions/%s" % self.subscription1.id, code=403, user=self.user2)

            self._send_get("/v1/news-subscriptions/%s" % self.subscription2.id, code=403, user=self.user2)

            response = self._send_get('/v1/news/666', code=404, user=self.admin)

    def test_delete_list(self):
        """
        Check NewsSubscription: DELETE list
        """
        with app.test_request_context():
            self._blend()
            self._blend_subscription()
            self._send_delete("/v1/news-subscriptions", code=405)
            self._send_delete("/v1/news-subscriptions", code=405, user=self.admin)
            self._send_delete("/v1/news-subscriptions", code=405, user=self.user1)
            self._send_delete("/v1/news-subscriptions", code=405, user=self.user2)

    def test_delete_anonymous(self):
        """
        Check NewsSubscription: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend()
            self._blend_subscription()
            self._send_delete("/v1/news-subscriptions/1", code=401)
            self._send_delete("/v1/news-subscriptions/2", code=401)
            self._send_delete("/v1/news-subscriptions/3", code=404)

    def test_delete_admin(self):
        """
        Check NewsSubscription: DELETE Admin
        """
        with app.test_request_context():
            self._blend()
            self._blend_subscription()
            self._send_delete("/v1/news-subscriptions/1", code=200, user=self.admin)
            self._send_delete("/v1/news-subscriptions/2", code=200, user=self.admin)
            self._send_delete("/v1/news-subscriptions/3", code=404, user=self.admin)

    def test_delete_user1(self):
        """
        Check NewsSubscription: DELETE User1
        """
        with app.test_request_context():
            self._blend()
            self._blend_subscription()
            self._send_delete("/v1/news-subscriptions/1", code=403, user=self.user1)
            self._send_delete("/v1/news-subscriptions/2", code=200, user=self.user1)
            self._send_delete("/v1/news-subscriptions/3", code=404, user=self.user1)

    def test_delete_user2(self):
        """
        Check NewsSubscription: DELETE User2
        """
        with app.test_request_context():
            self._blend()
            self._blend_subscription()
            self._send_delete("/v1/news-subscriptions/1", code=403, user=self.user2)
            self._send_delete("/v1/news-subscriptions/2", code=403, user=self.user2)
            self._send_delete("/v1/news-subscriptions/3", code=404, user=self.user2)
