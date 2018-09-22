# -*- coding: utf-8 -*-

from datetime import timedelta

from flask_rest_jsonapi.exceptions import ObjectNotFound
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPES_TEXT,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_DIPPED)
from app.api.helpers.db import safe_query
from app.models.move import Move
from tests.unittests.utils import assertIsDateTime
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_type)
from tests.unittests.utils.payload.geokret import GeokretyPayload
from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestGeokretCreate(BaseTestCase):
    """Test Geokrety creation"""

    def _send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return GeokretResponse(super(TestGeokretCreate, self)._send_post(
            "/v1/geokrety",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    # ## TEST CASES ##

    def test_geokret_create_as_anonymous_user(self):
        payload = GeokretyPayload()
        assert self._send_post(payload, user=None, code=401)

    def test_geokret_create_as_authenticated_user(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            assert self._send_post(payload, user=self.user_1)

    def test_geokret_create_field_creation_date_time_is_auto_managed(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1)
            response.assertCreationDateTime()

    def test_geokret_create_field_update_date_time_is_auto_managed(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1)
            response.assertUpdatedDateTime()

    def test_geokret_create_field_creation_date_time_is_equal_to_update_date_time(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1)
            self.assertAlmostEqual(
                response.created_on_datetime,
                response.updated_on_datetime,
                delta=timedelta(seconds=1)
            )

    def test_geokret_create_owner_is_the_connected_user_if_undefined(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1)
            response.pprint()
            response.assertHasRelationshipOwnerData(self.user_1.id)

    def test_geokret_create_owner_is_the_connected_user_if_undefined_even_for_admin(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.admin)
            response.assertHasRelationshipOwnerData(self.admin.id)

    def test_geokret_create_owner_enforced_to_current_user(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            user_2 = self.blend_user()
            payload.set_owner(user_2)
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasRelationshipOwnerData(self.user_1.id)

    def test_geokret_create_owner_enforced_by_admin(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            payload.set_owner(self.user_1)
            response = self._send_post(payload, user=self.admin, code=201)
            response.assertHasRelationshipOwnerData(self.user_1.id)

    @parameterized.expand([
        [GEOKRET_TYPE_TRADITIONAL],
        [GEOKRET_TYPE_BOOK],
        [GEOKRET_TYPE_HUMAN],
        [GEOKRET_TYPE_COIN],
        [GEOKRET_TYPE_KRETYPOST],
    ], doc_func=custom_name_geokrety_type)
    def test_geokret_create_geokrety_type_exists(self, geokret_type):
        payload = GeokretyPayload()
        payload.set_geokrety_type(geokret_type)
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.admin)
            response.assertHasRelationshipGeokretyType()

    @parameterized.expand([
        [666],
        ["A"],
        ["777"],
        [u"yjgdf"],
        [u"ginieḰ"],
        [u""],
    ])
    def test_geokret_create_geokrety_type_non_existent(self, geokret_type):
        payload = GeokretyPayload()
        payload.set_geokrety_type(geokret_type)
        with app.test_request_context():
            self.blend_users()
            self._send_post(payload, user=self.admin, code=422)

    def test_geokret_create_field_name_must_be_present(self):
        payload = GeokretyPayload()
        del payload['data']['attributes']['name']
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=422)
            response.assertRaiseJsonApiError('/data/attributes/name')

    @parameterized.expand(EMPTY_TEST_CASES)
    def test_geokret_create_field_name_cannot_be_blank(self, name):
        payload = GeokretyPayload()
        payload.set_name(name)
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=422)
            response.assertRaiseJsonApiError('/data/attributes/name')

    @parameterized.expand(UTF8_TEST_CASES)
    def test_geokret_create_field_name_accept_unicode(self, name, result=None):
        payload = GeokretyPayload()
        payload.set_name(name)
        if result is None:
            result = name
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasAttribute('name', result)

    @parameterized.expand(NO_HTML_TEST_CASES)
    def test_geokret_create_field_name_doesnt_accept_html(self, name, result=None):
        payload = GeokretyPayload()
        payload.set_name(name)
        if result is None:
            result = name
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasAttribute('name', result)

    def test_geokret_create_field_description_may_be_absent(self):
        payload = GeokretyPayload()
        del payload['data']['attributes']['description']
        with app.test_request_context():
            self.blend_users()
            assert self._send_post(payload, user=self.user_1)

    @parameterized.expand(UTF8_TEST_CASES)
    def test_geokret_create_field_description_accept_unicode(self, description, result=None):
        payload = GeokretyPayload()
        payload.set_description(description)
        if result is None:
            result = description
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasAttribute('description', result)

    @parameterized.expand(HTML_SUBSET_TEST_CASES)
    def test_geokret_create_field_description_accept_html_subset(self, description, result=None):
        payload = GeokretyPayload()
        payload.set_description(description)
        if result is None:
            result = description
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasAttribute('description', result)

    def test_geokret_create_holder_is_owner_for_himself(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.user_1, code=201)
            response.assertHasRelationshipHolderData(self.user_1.id)

    def test_geokret_create_holder_is_owner_for_himself_as_admin(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            response = self._send_post(payload, user=self.admin, code=201)
            response.assertHasRelationshipHolderData(self.admin.id)

    def test_geokret_create_holder_is_owner_for_someone_else_by_admin(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            self.blend_users()
            payload.set_owner(self.user_1)
            response = self._send_post(payload, user=self.admin, code=201)
            response.assertHasRelationshipHolderData(self.user_1.id)

    def test_geokret_create_geokret_may_be_born_at_home_no_home_coordinates(self):
        payload = GeokretyPayload()
        with app.test_request_context():
            user = self.blend_user()
            response = self._send_post(payload, user=user, code=201)
            with self.assertRaises(ObjectNotFound):
                safe_query(self, Move, 'geokret_id', response.id, 'geokret_id')

    def test_geokret_create_geokret_may_be_born_at_home_with_home_coordinates(self):
        payload = GeokretyPayload()
        payload.set_born_at_home()
        with app.test_request_context():
            user = self.blend_user(latitude=48.8566, longitude=2.3522)
            response = self._send_post(payload, user=user, code=201)
            response.assertHasRelationshipMoves()
            move = safe_query(self, Move, 'geokret_id', response.id, 'geokret_id')
            self.assertEqual(move.move_type_id, MOVE_TYPE_DIPPED)
            self.assertEqual(move.latitude, user.latitude)
            self.assertEqual(move.longitude, user.longitude)
            assertIsDateTime(move.moved_on_datetime)
            self.assertEqual(move.author_id, user.id)
            self.assertEqual(move.comment, "Born here")
