from app import current_app as app
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestUser(GeokretyTestCase):
    """Test User CRUD operations"""

    def _blend(self):
        """Create mocked User/News/NewsComments"""
        mixer.init_app(app)
        self.admin = mixer.blend(User)
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)
        self.news1 = mixer.blend(News, author=self.user1)
        # self.news2 = mixer.blend(News)
        self.orphan_news = mixer.blend(News, author=None)
        self.newscomment1 = mixer.blend(NewsComment, author=self.user1, news=self.news1)
        # self.newscomment2 = mixer.blend(NewsComment, author=self.user2, news=self.news1)

    def _check_user(self, data, user, check_private_values=True):
        self.assertTrue('attributes' in data['data'])
        self.assertTrue('name' in data['data']['attributes'])
        attributes = data['data']['attributes']

        self.assertTrue('name' in attributes)
        self.assertTrue('country' in attributes)
        self.assertTrue('language' in attributes)
        self.assertTrue('statpic-id' in attributes)
        self.assertTrue('join-date-time' in attributes)
        self.assertFalse('password' in attributes)
        self.assertFalse('ip' in attributes)
        self.assertEqual(attributes['name'], user.name)
        self.assertEqual(attributes['language'], user.language)
        self.assertDateTimeEqual(attributes['join-date-time'], user.join_date_time)

        if check_private_values:
            self.assertEqual(attributes['country'], user.country)
            self.assertEqual(attributes['statpic-id'], user.statpic_id)

    def _check_user_with_private(self, data, user, check_private_values=True):
        self._check_user(data, user, check_private_values)
        attributes = data['data']['attributes']

        self.assertTrue('email' in attributes)
        self.assertTrue('hour' in attributes)
        self.assertTrue('latitude' in attributes)
        self.assertTrue('longitude' in attributes)
        self.assertTrue('observation-radius' in attributes)
        self.assertTrue('secid' in attributes)
        self.assertTrue('last-login-date-time' in attributes)
        self.assertTrue('last-mail-date-time' in attributes)
        self.assertTrue('last-update-date-time' in attributes)
        self.assertEqual(attributes['email'], user.email)

        if check_private_values:
            self.assertEqual(attributes['hour'], user.hour)
            self.assertEqual(attributes['latitude'], user.latitude)
            self.assertEqual(attributes['longitude'], user.longitude)
            self.assertEqual(attributes['observation-radius'], user.observation_radius)
            self.assertEqual(attributes['secid'], user.secid)

            if attributes['last-login-date-time']:
                self.assertDateTimeEqual(attributes['last-login-date-time'], user.last_login_date_time)
            if attributes['last-mail-date-time']:
                self.assertDateTimeEqual(attributes['last-mail-date-time'], user.last_mail_date_time)
            if attributes['last-update-date-time']:
                self.assertDateTimeEqual(attributes['last-update-date-time'], user.last_update_date_time)

    def _check_user_without_private(self, data, user, check_private_values=True):
        self._check_user(data, user, check_private_values)
        attributes = data['data']['attributes']

        self.assertFalse('email' in attributes)
        self.assertFalse('hour' in attributes)
        self.assertFalse('latitude' in attributes)
        self.assertFalse('longitude' in attributes)
        self.assertFalse('observation-radius' in attributes)
        self.assertFalse('secid' in attributes)
        self.assertFalse('last-login-date-time' in attributes)
        self.assertFalse('last-mail-date-time' in attributes)
        self.assertFalse('last-update-date-time' in attributes)

    def test_post_content_types(self):
        """Check accepted content types"""
        self._send_post("/v1/users", payload="not a json", code=415, content_type='application/json')
        self._send_post("/v1/users", payload={}, code=422)
        self._send_post("/v1/users", payload={"user": "kumy"}, code=422)

    def test_create_incomplete(self):
        """Check incomplete create request"""
        payload = {
            "data": {
                "type": "user"
            }
        }
        self._send_post("/v1/users", payload=payload, code=500)  # TODO should not be a 500

    def test_create_minimal(self):
        """Check create request minimal informations"""
        with app.test_request_context():
            with mixer.ctx(commit=False):
                someone = mixer.blend(User)

            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                            "name": someone.name,
                            "password": someone.password,
                            "email": someone.email
                    }
                }
            }
            response = self._send_post("/v1/users", payload=payload, code=201)
            self._check_user_with_private(response, someone, check_private_values=False)

            users = User.query.all()
            self.assertEqual(len(users), 1)
            user = users[0]
            self.assertEqual(someone.name, user.name)
            self._check_user_with_private(response, user)

    def test_create_complete(self):
        """Check create request full informations"""
        with app.test_request_context():
            with mixer.ctx(commit=False):
                someone = mixer.blend(User)

            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                            "name": someone.name,
                            "password": someone.password,
                            "email": someone.email,
                            "hour": someone.hour,
                            "latitude": someone.latitude,
                            "longitude": someone.longitude,
                            "observation-radius": someone.observation_radius,
                            "secid": someone.secid,
                            "statpic-id": someone.statpic_id
                    }
                }
            }
            response = self._send_post("/v1/users", payload=payload, code=201)
            self._check_user_with_private(response, someone, check_private_values=False)

            users = User.query.all()
            self.assertEqual(len(users), 1)
            user = users[0]
            self.assertEqual(someone.name, user.name)
            self._check_user_with_private(response, user)

    def test_create_user(self):
        """Check create and Read back an user"""
        with app.test_request_context():
            mixer.init_app(app)
            admin = mixer.blend(User)
            someone = mixer.blend(User)
            with mixer.ctx(commit=False):
                user1 = mixer.blend(User)

            # Test inserting first user
            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                        "name": user1.name,
                        "password": user1.password,
                        "email": user1.email
                    }
                }
            }
            response = self._send_post('/v1/users', payload=payload, code=201)
            self._check_user_with_private(response, user1, check_private_values=False)
            user1.id = response['data']['id']

            response = self._send_get('/v1/users/%s' % user1.id, code=200)
            self._check_user_without_private(response, user1, check_private_values=False)

            response = self._send_get('/v1/users/%s' % user1.id, code=200, user=user1)
            self._check_user_with_private(response, user1, check_private_values=False)

            response = self._send_get('/v1/users/%s' % user1.id, code=200, user=admin)
            self._check_user_with_private(response, user1, check_private_values=False)

            response = self._send_get('/v1/users/%s' % user1.id, code=200, user=someone)
            self._check_user_without_private(response, user1, check_private_values=False)

    def test_create_user_name_uniqueness(self):
        """Check create user, name uniqueness"""
        with app.test_request_context():
            self._blend()
            with mixer.ctx(commit=False):
                user1 = mixer.blend(User)

            # Test inserting first user
            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                        "name": self.user1.name,
                        "password": user1.password,
                        "email": user1.email
                    }
                }
            }
            self._send_post('/v1/users', payload=payload, code=422)

    def test_create_user_email_uniqueness(self):
        """Check create user, email uniqueness"""
        with app.test_request_context():
            self._blend()
            with mixer.ctx(commit=False):
                user1 = mixer.blend(User)

            # Test inserting first user
            payload = {
                "data": {
                    "type": "user",
                    "attributes": {
                        "name": user1.name,
                        "password": user1.password,
                        "email": self.user1.email
                    }
                }
            }
            self._send_post('/v1/users', payload=payload, code=422)

    def test_get_user_list(self):
        """Check GET user listing must be authenticated"""
        with app.test_request_context():
            self._blend()
            self._send_get('/v1/users', code=401)
            self._send_get('/v1/users', code=200, user=self.admin)
            self._send_get('/v1/users', code=403, user=self.user1)
            self._send_get('/v1/users', code=403, user=self.user2)

    def test_get_user_details(self):
        """Check GET user details"""
        with app.test_request_context():
            self._blend()
            url = '/v1/users/%d' % self.user1.id

            response = self._send_get(url, code=200)
            self._check_user_without_private(response, self.user1)

            response = self._send_get(url, code=200, user=self.admin)
            self._check_user_with_private(response, self.user1)

            response = self._send_get(url, code=200, user=self.user1)
            self._check_user_with_private(response, self.user1)

            response = self._send_get(url, code=200, user=self.user2)
            self._check_user_without_private(response, self.user1)

    def test_get_news_author(self):
        """Check GET author details from a news"""
        with app.test_request_context():
            self._blend()
            url = '/v1/news/%d/author' % self.news1.id

            response = self._send_get(url, code=200)
            self._check_user_without_private(response, self.user1)
            response = self._send_get(url, code=200, user=self.admin)
            self._check_user_with_private(response, self.user1)
            response = self._send_get(url, code=200, user=self.user1)
            self._check_user_with_private(response, self.user1)
            response = self._send_get(url, code=200, user=self.user2)
            self._check_user_without_private(response, self.user1)

    def test_get_unexistent_news_author(self):
        """Check GET author details from an unexistent news"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/news/666/author', code=404, user=self.admin)
            self._send_get('/v1/news/666/author', code=404, user=self.user1)
            self._send_get('/v1/news/666/author', code=404, user=self.user2)

    def test_get_news_orphan(self):
        """Check GET author details from an orphan news"""
        with app.test_request_context():
            self._blend()
            orphan_url = '/v1/news/%d/author' % self.orphan_news.id

            self._send_get(orphan_url, code=404, user=self.admin)
            self._send_get(orphan_url, code=404, user=self.user1)
            self._send_get(orphan_url, code=404, user=self.user2)

    def test_get_news_comment_author(self):
        """Check GET author from a news_comment"""
        with app.test_request_context():
            self._blend()
            response = self._send_get('/v1/news-comments/1/author', code=200, user=self.admin)
            self._check_user_with_private(response, self.user1)
            response = self._send_get('/v1/news-comments/1/author', code=200, user=self.user1)
            self._check_user_with_private(response, self.user1)
            response = self._send_get('/v1/news-comments/1/author', code=200, user=self.user2)
            self._check_user_without_private(response, self.user1)

            self._send_get('/v1/news-comments/666/author', code=404, user=self.admin)
            self._send_get('/v1/news-comments/666/author', code=404, user=self.user1)
            self._send_get('/v1/news-comments/666/author', code=404, user=self.user2)

    def test_patch_list(self):
        """
        Check patch list cannot be patched
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/users", code=405)
            self._send_patch("/v1/users", code=405, user=self.admin)
            self._send_patch("/v1/users", code=405, user=self.user1)
            self._send_patch("/v1/users", code=405, user=self.user2)

    def test_patch_anonymous(self):
        """
        Check patch anonymously is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/users", code=405)
            self._send_patch("/v1/users/1", code=401)
            self._send_patch("/v1/users/2", code=401)
            self._send_patch("/v1/users/3", code=401)
            self._send_patch("/v1/users/4", code=401)

    def test_patch_full_admin_someone(self):
        """
        Check patch admin can update everyone - Admin
        """
        with app.test_request_context():
            self._blend()
            with mixer.ctx(commit=False):
                someone = mixer.blend(User)

            payload = {
                "data": {
                    "type": "user",
                    "id": None,
                    "attributes": {
                            "name": None,
                            "password": someone.password,
                            "email": None,
                            "hour": someone.hour,
                            "latitude": someone.latitude,
                            "longitude": someone.longitude,
                            "observation-radius": someone.observation_radius,
                            "secid": someone.secid,
                            "statpic-id": someone.statpic_id
                    }
                }
            }

            payload["data"]["id"] = "1"
            payload["data"]["attributes"]["name"] = "someone_1"
            payload["data"]["attributes"]["email"] = "someone_1@email.email"
            self._send_patch("/v1/users/1", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = "someone_2"
            payload["data"]["attributes"]["email"] = "someone_2@email.email"
            self._send_patch("/v1/users/2", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = "someone_3"
            payload["data"]["attributes"]["email"] = "someone_3@email.email"
            self._send_patch("/v1/users/3", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "someone_4"
            payload["data"]["attributes"]["email"] = "someone_4@email.email"
            self._send_patch("/v1/users/4", payload=payload, code=404, user=self.admin)

    def test_patch_full_user1_someone(self):
        """
        Check patch user can only update himself - User1
        """
        with app.test_request_context():
            self._blend()
            with mixer.ctx(commit=False):
                someone = mixer.blend(User)

            payload = {
                "data": {
                    "type": "user",
                    "id": "2",
                    "attributes": {
                            "name": someone.name,
                            "password": someone.password,
                            "email": someone.email,
                            "hour": someone.hour,
                            "latitude": someone.latitude,
                            "longitude": someone.longitude,
                            "observation-radius": someone.observation_radius,
                            "secid": someone.secid,
                            "statpic-id": someone.statpic_id
                    }
                }
            }

            payload["data"]["id"] = "1"
            payload["data"]["attributes"]["name"] = "someone_1"
            payload["data"]["attributes"]["email"] = "someone_1@email.email"
            self._send_patch("/v1/users/1", payload=payload, code=403, user=self.user1)

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = "someone_2"
            payload["data"]["attributes"]["email"] = "someone_2@email.email"
            self._send_patch("/v1/users/2", payload=payload, code=200, user=self.user1)

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = "someone_3"
            payload["data"]["attributes"]["email"] = "someone_3@email.email"
            self._send_patch("/v1/users/3", payload=payload, code=403, user=self.user1)

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "someone_4"
            payload["data"]["attributes"]["email"] = "someone_4@email.email"
            self._send_patch("/v1/users/4", payload=payload, code=403, user=self.user1)

    def test_patch_same_username_admin(self):
        """
        Check patch username uniqueness - Admin
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "user",
                    "id": "1",
                    "attributes": {
                        "name": "someone"
                    }
                }
            }
            self._send_patch("/v1/users/1", payload=payload, code=200, user=self.admin)
            payload["data"]["id"] = "2"
            self._send_patch("/v1/users/2", payload=payload, code=422, user=self.admin)
            payload["data"]["id"] = "3"
            self._send_patch("/v1/users/3", payload=payload, code=422, user=self.admin)
            payload["data"]["id"] = "4"
            self._send_patch("/v1/users/4", payload=payload, code=422, user=self.admin)

    def test_patch_same_username_user1(self):
        """
        Check patch username uniqueness - User1
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "user",
                    "id": self.user1.id,
                    "attributes": {
                        "name": self.user2.name
                    }
                }
            }
            self._send_patch("/v1/users/%s" % self.user1.id, payload=payload, code=422, user=self.user1)

    def test_patch_same_email_admin(self):
        """
        Check patch email uniqueness - Admin
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "user",
                    "id": "1",
                    "attributes": {
                        "email": "someone@email.email"
                    }
                }
            }
            self._send_patch("/v1/users/1", payload=payload, code=200, user=self.admin)
            payload["data"]["id"] = "2"
            self._send_patch("/v1/users/2", payload=payload, code=422, user=self.admin)
            payload["data"]["id"] = "3"
            self._send_patch("/v1/users/3", payload=payload, code=422, user=self.admin)
            payload["data"]["id"] = "4"
            self._send_patch("/v1/users/4", payload=payload, code=422, user=self.admin)

    def test_patch_same_email_user1(self):
        """
        Check patch email uniqueness - User1
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "user",
                    "id": self.user1.id,
                    "attributes": {
                        "email": self.user2.email
                    }
                }
            }
            self._send_patch("/v1/users/%s" % self.user1.id, payload=payload, code=422, user=self.user1)

    def test_patch_id_must_match(self):
        """
        Check patch id must match
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "user",
                    "id": "1",
                    "attributes": {
                        "secid": "some ultra secret string"
                    }
                }
            }
            self._send_patch("/v1/users/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/users/2", payload=payload, code=400, user=self.admin)
            self._send_patch("/v1/users/3", payload=payload, code=400, user=self.admin)
            self._send_patch("/v1/users/4", payload=payload, code=400, user=self.admin)

    def test_delete_list(self):
        """
        Check delete list
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/users", code=405)
            self._send_delete("/v1/users", code=405, user=self.admin)
            self._send_delete("/v1/users", code=405, user=self.user1)
            self._send_delete("/v1/users", code=405, user=self.user2)

    def test_delete_anonymous(self):
        """
        Check delete Anonymous
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/users/1", code=405)
            self._send_delete("/v1/users/2", code=405)
            self._send_delete("/v1/users/3", code=405)
            self._send_delete("/v1/users/4", code=405)

    def test_delete_admin(self):
        """
        Check delete Admin
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/users/1", code=405, user=self.admin)
            self._send_delete("/v1/users/2", code=405, user=self.admin)
            self._send_delete("/v1/users/3", code=405, user=self.admin)
            self._send_delete("/v1/users/4", code=405, user=self.admin)

    def test_delete_user1(self):
        """
        Check delete User1
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/users/1", code=405, user=self.user1)
            self._send_delete("/v1/users/2", code=405, user=self.user1)
            self._send_delete("/v1/users/3", code=405, user=self.user1)
            self._send_delete("/v1/users/4", code=405, user=self.user1)

    def test_delete_user2(self):
        """
        Check delete User2
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/users/1", code=405, user=self.user2)
            self._send_delete("/v1/users/2", code=405, user=self.user2)
            self._send_delete("/v1/users/3", code=405, user=self.user2)
            self._send_delete("/v1/users/4", code=405, user=self.user2)
