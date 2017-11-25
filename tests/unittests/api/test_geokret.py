from app import current_app as app
# from app.api.helpers.db import safe_query
from app.models import db
from app.models.geokret import Geokret
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestGeokret(GeokretyTestCase):
    """Test GeoKret CRUD operations"""

    def _blend(self):
        """Create mocked Geokret/User"""
        mixer.init_app(app)
        with mixer.ctx(commit=False):
            self.admin = mixer.blend(User)
            self.user1 = mixer.blend(User)
            self.user2 = mixer.blend(User)
            self.geokret1 = mixer.blend(Geokret, owner=self.user1)
            self.geokret2 = mixer.blend(Geokret, owner=self.user2)
            self.geokret3 = mixer.blend(Geokret)
            db.session.add(self.admin)
            db.session.add(self.user1)
            db.session.add(self.user2)
            db.session.add(self.geokret1)
            db.session.add(self.geokret2)
            db.session.add(self.geokret3)
            db.session.commit()

    def _check_geokret_with_private(self, data, geokret, skip_check=None):
        skip_check = skip_check or []
        # self.assertTrue('attributes' in data['data'])
        # attributes = data['data']['attributes']
        self.assertTrue('attributes' in data)
        attributes = data['attributes']

        self.assertTrue('tracking-code' in attributes)

        if 'tracking-code' not in skip_check:
            self.assertEqual(attributes['tracking-code'], geokret.tracking_code)

        self._check_geokret_without_private(data, geokret, skip_check)

    def _check_geokret_without_private(self, data, geokret, skip_check=None):
        skip_check = skip_check or []
        # self.assertTrue('attributes' in data['data'])
        # attributes = data['data']['attributes']
        self.assertTrue('attributes' in data)
        attributes = data['attributes']

        self.assertTrue('name' in attributes)
        self.assertTrue('description' in attributes)
        self.assertTrue('missing' in attributes)
        self.assertTrue('distance' in attributes)
        self.assertTrue('caches-count' in attributes)
        self.assertTrue('pictures-count' in attributes)
        self.assertTrue('average-rating' in attributes)
        self.assertTrue('created-on-date-time' in attributes)
        self.assertTrue('updated-on-date-time' in attributes)

        self.assertEqual(attributes['name'], geokret.name)
        self.assertEqual(attributes['description'], geokret.description)
        self.assertEqual(attributes['missing'], geokret.missing)
        self.assertEqual(attributes['distance'], geokret.distance)
        self.assertEqual(attributes['caches-count'], geokret.caches_count)
        self.assertEqual(attributes['pictures-count'], geokret.pictures_count)
        self.assertEqual(attributes['average-rating'], geokret.average_rating)

        if 'times' not in skip_check:
            self.assertDateTimeEqual(attributes['created-on-date-time'], geokret.created_on_date_time)
            self.assertDateTimeEqual(attributes['updated-on-date-time'], geokret.updated_on_date_time)

    def test_create_authenticated_only(self):
        """Check Geokret: POST is reserved to authenticated users"""
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                        "name": "akret.name"
                    }
                }
            }
            self._send_post("/v1/geokrety", payload=payload, code=401)
            self._send_post("/v1/geokrety", payload=payload, code=201, user=self.admin)
            self._send_post("/v1/geokrety", payload=payload, code=201, user=self.user1)
            self._send_post("/v1/geokrety", payload=payload, code=201, user=self.user2)

    def test_post_content_types(self):
        """Check Geokret: POST accepted content types"""
        with app.test_request_context():
            admin = mixer.blend(User)
            self._send_post("/v1/geokrety", payload="not a json", code=415, content_type='application/json', user=admin)
            self._send_post("/v1/geokrety", payload={}, code=422, user=admin)
            self._send_post("/v1/geokrety", payload={"description": "missing mandatory attributes"},
                            code=422, user=admin)

    def test_create_incomplete(self):
        """Check Geokret: POST incomplete request"""
        with app.test_request_context():
            admin = mixer.blend(User)
            payload = {
                "data": {
                    "type": "geokret"
                }
            }
            self._send_post("/v1/geokrety", payload=payload, code=422, user=admin)

    def test_create_invalid(self):
        """Check Geokret: POST invalid request"""
        with app.test_request_context():
            admin = mixer.blend(User)
            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": 0,
                            "description": 0,
                    }
                }
            }
            self._send_post("/v1/geokrety", payload=payload, code=422, user=admin)

    def test_create_without_name(self):
        """Check Geokret: POST request without name"""
        with app.test_request_context():
            admin = mixer.blend(User)
            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "description": "we miss a name ;)"
                    }
                }
            }
            self._send_post("/v1/geokrety", payload=payload, code=422, user=admin)

    def test_create_minimal(self):
        """Check Geokret: POST request minimal informations"""
        with app.test_request_context():
            admin = mixer.blend(User)
            with mixer.ctx(commit=False):
                akret = mixer.blend(Geokret)

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                        "name": akret.name
                    }
                }
            }
            response = self._send_post("/v1/geokrety", payload=payload, code=201, user=admin)
            self._check_geokret_with_private(response['data'], akret, skip_check=['times', 'tracking-code'])

            geokrety = Geokret.query.all()
            self.assertEqual(len(geokrety), 1)
            geokret = geokrety[0]
            self.assertEqual(akret.name, geokret.name)
            self._check_geokret_with_private(response['data'], geokret)

    def test_create_complete(self):
        """Check Geokret: POST request full informations"""
        with app.test_request_context():
            admin = mixer.blend(User)
            with mixer.ctx(commit=False):
                akret = mixer.blend(Geokret)

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": akret.name,
                            "description": akret.description,
                    }
                }
            }
            response = self._send_post("/v1/geokrety", payload=payload, code=201, user=admin)
            self._check_geokret_with_private(response['data'], akret, skip_check=['times', 'tracking-code'])

            geokrety = Geokret.query.all()
            self.assertEqual(len(geokrety), 1)
            geokret = geokrety[0]
            self.assertEqual(akret.name, geokret.name)
            self._check_geokret_with_private(response['data'], geokret)

    def test_create_geokret(self):
        """ Check Geokret: POST and Read back a geokret"""
        with app.test_request_context():
            mixer.init_app(app)
            admin = mixer.blend(User)
            someone = mixer.blend(User)
            with mixer.ctx(commit=False):
                akret = mixer.blend(Geokret)

            # Test inserting first user
            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": akret.name,
                            "description": akret.description,
                    }
                }
            }
            response = self._send_post('/v1/geokrety', payload=payload, code=201, user=admin)
            self._check_geokret_with_private(response['data'], akret, skip_check=['times', 'tracking-code'])
            akret.id = response['data']['id']
            akret.tracking_code = response['data']['attributes']['tracking-code']

            response = self._send_get('/v1/geokrety/%s' % akret.id, code=200)
            self._check_geokret_without_private(response['data'], akret, skip_check=['times'])

            response = self._send_get('/v1/geokrety/%s' % akret.id, code=200, user=someone)
            self._check_geokret_without_private(response['data'], akret, skip_check=['times'])

            response = self._send_get('/v1/geokrety/%s' % akret.id, code=200, user=admin)
            self._check_geokret_with_private(response['data'], akret, skip_check=['times'])

    def test_create_geokret_ignore_non_writable_fields(self):
        """ Check Geokret: POST ignore non writable fields"""
        with app.test_request_context():
            admin = mixer.blend(User)
            with app.test_request_context():
                # Test inserting first user
                payload = {
                    "data": {
                        "type": "geokret",
                        "attributes": {
                            "name": "name",
                            "description": "description",
                            "tracking-code": "NOLUCK",
                            "missing": True,
                            "distance": 12,
                            "caches-count": 8,
                            "pictures-count": 82,
                            "average-rating": 4,
                            "created-on-date-time": "2007-10-26T20:36:00",
                            "updated-on-date-time": "2017-11-24T21:31:24"
                        }
                    }
                }
                self._send_post('/v1/geokrety', payload=payload, code=201, user=admin)

                geokrety = Geokret.query.all()
                self.assertEqual(len(geokrety), 1)
                geokret = geokrety[0]

                attributes = payload["data"]["attributes"]
                self.assertEqual(attributes["name"], geokret.name)
                self.assertEqual(attributes["description"], geokret.description)
                self.assertNotEqual(attributes["tracking-code"], geokret.tracking_code)
                self.assertNotEqual(attributes["missing"], geokret.missing)
                self.assertNotEqual(attributes["distance"], geokret.distance)
                self.assertNotEqual(attributes["caches-count"], geokret.caches_count)
                self.assertNotEqual(attributes["pictures-count"], geokret.pictures_count)
                self.assertNotEqual(attributes["average-rating"], geokret.average_rating)
                self.assertNotEqual(attributes["created-on-date-time"], geokret.created_on_date_time)
                self.assertNotEqual(attributes["updated-on-date-time"], geokret.updated_on_date_time)

    def test_create_geokret_verify_tracking_code(self):
        """ Check Geokret: VERIFY tracking_code"""
        with app.test_request_context():
            geokret1 = mixer.blend(Geokret)
            geokret2 = mixer.blend(Geokret)
            geokret3 = mixer.blend(Geokret)

            self.assertNotEqual(geokret1.tracking_code, geokret2.tracking_code)
            self.assertNotEqual(geokret1.tracking_code, geokret3.tracking_code)
            self.assertIsNotNone(geokret1.tracking_code)
            self.assertIsNotNone(geokret2.tracking_code)
            self.assertIsNotNone(geokret3.tracking_code)
            self.assertGreaterEqual(len(geokret1.tracking_code), 6)
            self.assertGreaterEqual(len(geokret2.tracking_code), 6)
            self.assertGreaterEqual(len(geokret3.tracking_code), 6)

    def test_get_geokrety_list(self):
        """ Check Geokret: GET geokrety list"""
        with app.test_request_context():
            self._blend()

            response = self._send_get('/v1/geokrety', code=200)['data']
            self.assertEqual(len(response), 3)
            self._check_geokret_without_private(response[0], self.geokret1)
            self._check_geokret_without_private(response[1], self.geokret2)
            self._check_geokret_without_private(response[2], self.geokret3)

            response = self._send_get('/v1/geokrety', code=200, user=self.admin)['data']
            self.assertEqual(len(response), 3)
            self._check_geokret_with_private(response[0], self.geokret1)
            self._check_geokret_with_private(response[1], self.geokret2)
            self._check_geokret_with_private(response[2], self.geokret3)

            response = self._send_get('/v1/geokrety', code=200, user=self.user1)['data']
            self.assertEqual(len(response), 3)
            self._check_geokret_without_private(response[0], self.geokret1)
            self._check_geokret_without_private(response[1], self.geokret2)
            self._check_geokret_without_private(response[2], self.geokret3)

            response = self._send_get('/v1/geokrety', code=200, user=self.user2)['data']
            self.assertEqual(len(response), 3)
            self._check_geokret_without_private(response[0], self.geokret1)
            self._check_geokret_without_private(response[1], self.geokret2)
            self._check_geokret_without_private(response[2], self.geokret3)

    def test_get_geokrety_details(self):
        """ Check Geokret: GET geokrety details"""
        with app.test_request_context():
            self._blend()
            url = '/v1/geokrety/%d' % self.geokret1.id

            response = self._send_get(url, code=200)
            self._check_geokret_without_private(response['data'], self.geokret1)

            response = self._send_get(url, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret1)

            response = self._send_get(url, code=200, user=self.user1)
            self._check_geokret_with_private(response['data'], self.geokret1)

            response = self._send_get(url, code=200, user=self.user2)
            self._check_geokret_without_private(response['data'], self.geokret1)

    # def test_get_news_author(self):
    #     """ Check Geokret: GET author details from a news"""
    #     with app.test_request_context():
    #         self._blend()
    #         url = '/v1/news/%d/author' % self.news1.id
    #
    #         response = self._send_get(url, code=200)
    #         self._check_user_without_private(response, self.user1)
    #         response = self._send_get(url, code=200, user=self.admin)
    #         self._check_user_with_private(response, self.user1)
    #         response = self._send_get(url, code=200, user=self.user1)
    #         self._check_user_with_private(response, self.user1)
    #         response = self._send_get(url, code=200, user=self.user2)
    #         self._check_user_without_private(response, self.user1)
    #
    # def test_get_unexistent_news_author(self):
    #     """ Check Geokret: GET author details from an unexistent news"""
    #     with app.test_request_context():
    #         self._blend()
    #
    #         self._send_get('/v1/news/666/author', code=404, user=self.admin)
    #         self._send_get('/v1/news/666/author', code=404, user=self.user1)
    #         self._send_get('/v1/news/666/author', code=404, user=self.user2)
    #
    # def test_get_news_orphan(self):
    #     """ Check Geokret: GET author details from an orphan news"""
    #     with app.test_request_context():
    #         self._blend()
    #         orphan_url = '/v1/news/%d/author' % self.orphan_news.id
    #
    #         self._send_get(orphan_url, code=404, user=self.admin)
    #         self._send_get(orphan_url, code=404, user=self.user1)
    #         self._send_get(orphan_url, code=404, user=self.user2)
    #
    # def test_get_news_comment_author(self):
    #     """ Check Geokret: GET author from a news_comment"""
    #     with app.test_request_context():
    #         self._blend()
    #         response = self._send_get('/v1/news-comments/1/author', code=200, user=self.admin)
    #         self._check_user_with_private(response, self.user1)
    #         response = self._send_get('/v1/news-comments/1/author', code=200, user=self.user1)
    #         self._check_user_with_private(response, self.user1)
    #         response = self._send_get('/v1/news-comments/1/author', code=200, user=self.user2)
    #         self._check_user_without_private(response, self.user1)
    #
    #         self._send_get('/v1/news-comments/666/author', code=404, user=self.admin)
    #         self._send_get('/v1/news-comments/666/author', code=404, user=self.user1)
    #         self._send_get('/v1/news-comments/666/author', code=404, user=self.user2)

    def test_patch_list(self):
        """
        Check Geokret: PATCH list cannot be patched
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/geokrety", code=405)
            self._send_patch("/v1/geokrety", code=405, user=self.admin)
            self._send_patch("/v1/geokrety", code=405, user=self.user1)
            self._send_patch("/v1/geokrety", code=405, user=self.user2)

    def test_patch_anonymous(self):
        """
        Check Geokret: PATCH anonymously is forbidden
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/geokrety", code=405)
            self._send_patch("/v1/geokrety/1", code=401)
            self._send_patch("/v1/geokrety/2", code=401)
            self._send_patch("/v1/geokrety/3", code=401)
            self._send_patch("/v1/geokrety/4", code=401)

    def test_patch_full_by_admin(self):
        """
        Check Geokret: PATCH admin can update every GeoKrety - Admin
        But limited to writable fields.
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": self.geokret1.name,
                            "description": self.geokret1.description,
                            "tracking-code": "NOLUCK",
                            "missing": False,
                            "distance": 42,
                            "caches-count": 12,
                            "pictures-count": 8,
                            "average-rating": 82,
                            "created-on-date-time": "2007-10-26T20:36:00",
                            "updated-on-date-time": "2017-11-25T13:45:18"
                    }
                }
            }

            payload["data"]["id"] = "1"
            payload["data"]["attributes"]["name"] = self.geokret1.name = "geokret_1"
            payload["data"]["attributes"]["description"] = self.geokret1.description = "description_1"
            response = self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret1, skip_check=['times'])

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = self.geokret2.name = "geokret_2"
            payload["data"]["attributes"]["description"] = self.geokret2.description = "description_2"
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = self.geokret3.name = "geokret_3"
            payload["data"]["attributes"]["description"] = self.geokret3.description = "description_3"
            response = self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret3, skip_check=['times'])

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "geokret_4"
            payload["data"]["attributes"]["description"] = "description_4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_full_by_user1(self):
        """
        Check Geokret: PATCH users can update GeoKrety they own - User1
        But limited to writable fields.
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": self.geokret1.name,
                            "description": self.geokret1.description,
                            "tracking-code": "NOLUCK",
                            "missing": False,
                            "distance": 42,
                            "caches-count": 12,
                            "pictures-count": 8,
                            "average-rating": 82,
                            "created-on-date-time": "2007-10-26T20:36:00",
                            "updated-on-date-time": "2017-11-25T13:45:18"
                    }
                }
            }

            payload["data"]["id"] = "1"
            payload["data"]["attributes"]["name"] = self.geokret1.name = "geokret_1"
            payload["data"]["attributes"]["description"] = self.geokret1.description = "description_1"
            response = self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.user1)
            self._check_geokret_with_private(response['data'], self.geokret1, skip_check=['times'])

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = self.geokret2.name = "geokret_2"
            payload["data"]["attributes"]["description"] = self.geokret2.email = "description_2"
            self._send_patch("/v1/geokrety/2", payload=payload, code=403, user=self.user1)

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = self.geokret3.name = "geokret_3"
            payload["data"]["attributes"]["description"] = self.geokret3.email = "description_3"
            self._send_patch("/v1/geokrety/3", payload=payload, code=403, user=self.user1)

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "geokret_4"
            payload["data"]["attributes"]["description"] = "description_4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.user1)

    def test_patch_full_by_user2(self):
        """
        Check Geokret: PATCH users can update GeoKrety they own - User2
        But limited to writable fields.
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "type": "geokret",
                    "attributes": {
                            "name": self.geokret2.name,
                            "description": self.geokret2.description,
                            "tracking-code": "NOLUCK",
                            "missing": False,
                            "distance": 42,
                            "caches-count": 12,
                            "pictures-count": 8,
                            "average-rating": 82,
                            "created-on-date-time": "2007-10-26T20:36:00",
                            "updated-on-date-time": "2017-11-25T13:45:18"
                    }
                }
            }

            payload["data"]["id"] = "1"
            payload["data"]["attributes"]["name"] = self.geokret1.name = "geokret_1"
            payload["data"]["attributes"]["description"] = self.geokret1.description = "description_1"
            self._send_patch("/v1/geokrety/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = self.geokret2.name = "geokret_2"
            payload["data"]["attributes"]["description"] = self.geokret2.description = "description_2"
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.user2)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = self.geokret3.name = "geokret_3"
            payload["data"]["attributes"]["description"] = self.geokret3.description = "description_3"
            self._send_patch("/v1/geokrety/3", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "geokret_4"
            payload["data"]["attributes"]["description"] = "description_4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.user2)

    def test_patch_geokret_name_individually(self):
        """
        Check Geokret: PATCH geokret name individually
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "id": "1",
                    "type": "geokret",
                    "attributes": {}
                }
            }
            payload["data"]["attributes"]["name"] = self.geokret1.name = "geokret1.name"
            response = self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret1, skip_check=['times'])

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = self.geokret2.name = "geokret2.name"
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = self.geokret3.name = "geokret3.name"
            response = self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret3, skip_check=['times'])

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["name"] = "geokret4.name"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_geokret_description_individually(self):
        """
        Check Geokret: PATCH geokret description individually
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "id": "1",
                    "type": "geokret",
                    "attributes": {
                            "description": ""
                    }
                }
            }
            print(self.geokret1.distance)
            payload["data"]["attributes"]["description"] = self.geokret1.description = "geokret1.description"
            response = self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret1, skip_check=['times'])

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["description"] = self.geokret2.description = "geokret2.description"
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["description"] = self.geokret3.description = "geokret3.description"
            response = self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret3, skip_check=['times'])

            payload["data"]["id"] = "4"
            payload["data"]["attributes"]["description"] = "geokret4.description"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_geokret_readonly_fields_ignored(self):
        """
        Check Geokret: PATCH geokret read only fields are ignored
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "id": "1",
                    "type": "geokret",
                    "attributes": {
                            "tracking-code": "NOLUCK",
                            "missing": False,
                            "distance": 42,
                            "caches-count": 12,
                            "pictures-count": 8,
                            "average-rating": 82,
                            "created-on-date-time": "2007-10-26T20:36:00",
                            "updated-on-date-time": "2017-11-25T13:45:18"
                    }
                }
            }
            response = self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret1, skip_check=['times'])

            payload["data"]["id"] = "2"
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            response = self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret3, skip_check=['times'])

            payload["data"]["id"] = "4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_same_geokret_name(self):
        """
        Check Geokret: PATCH geokret name can be repeated
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "id": "1",
                    "type": "geokret",
                    "attributes": {}
                }
            }

            payload["data"]["id"] = "2"
            payload["data"]["attributes"]["name"] = self.geokret2.name = self.geokret1.name
            response = self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret2, skip_check=['times'])

            payload["data"]["id"] = "3"
            payload["data"]["attributes"]["name"] = self.geokret3.name = self.geokret1.name
            response = self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)
            self._check_geokret_with_private(response['data'], self.geokret3, skip_check=['times'])

            payload["data"]["id"] = "4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_same_geokret_description(self):
        """
        Check Geokret: PATCH geokret description can be repeated
        """
        with app.test_request_context():
            self._blend()

            payload = {
                "data": {
                    "id": "1",
                    "type": "geokret",
                    "attributes": {
                            "description": self.geokret2.description
                    }
                }
            }
            self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/geokrety/2", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "3"
            self._send_patch("/v1/geokrety/3", payload=payload, code=200, user=self.admin)

            payload["data"]["id"] = "4"
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_patch_id_must_match(self):
        """
        Check Geokret: PATCH id must match
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "geokret",
                    "id": "1",
                    "attributes": {
                        "name": "GeoKret Name"
                    }
                }
            }
            self._send_patch("/v1/geokrety/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/geokrety/2", payload=payload, code=400, user=self.admin)
            self._send_patch("/v1/geokrety/3", payload=payload, code=400, user=self.admin)
            self._send_patch("/v1/geokrety/4", payload=payload, code=404, user=self.admin)

    def test_delete_list(self):
        """
        Check Geokret: DELETE list
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety", code=405)
            self._send_delete("/v1/geokrety", code=405, user=self.admin)
            self._send_delete("/v1/geokrety", code=405, user=self.user1)
            self._send_delete("/v1/geokrety", code=405, user=self.user2)

    def test_delete_anonymous(self):
        """
        Check Geokret: DELETE Anonymous
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety/1", code=401)
            self._send_delete("/v1/geokrety/2", code=401)
            self._send_delete("/v1/geokrety/3", code=401)
            self._send_delete("/v1/geokrety/4", code=401)

    def test_delete_admin(self):
        """
        Check Geokret: DELETE Admin
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety/1", code=200, user=self.admin)
            self._send_delete("/v1/geokrety/2", code=200, user=self.admin)
            self._send_delete("/v1/geokrety/3", code=200, user=self.admin)
            self._send_delete("/v1/geokrety/4", code=404, user=self.admin)

    def test_delete_user1(self):
        """
        Check Geokret: DELETE User1
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety/1", code=200, user=self.user1)
            self._send_delete("/v1/geokrety/2", code=403, user=self.user1)
            self._send_delete("/v1/geokrety/3", code=403, user=self.user1)
            self._send_delete("/v1/geokrety/4", code=404, user=self.user1)

    def test_delete_user2(self):
        """
        Check Geokret: DELETE User2
        """
        with app.test_request_context():
            self._blend()
            self._send_delete("/v1/geokrety/1", code=403, user=self.user2)
            self._send_delete("/v1/geokrety/2", code=200, user=self.user2)
            self._send_delete("/v1/geokrety/3", code=403, user=self.user2)
            self._send_delete("/v1/geokrety/4", code=404, user=self.user2)
