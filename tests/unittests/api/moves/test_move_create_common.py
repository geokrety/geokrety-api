# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED,
                                         MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  request_context)
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.static_test_cases import (BLANK_CHARACTERS_TEST_CASES,
                                                     EMPTY_TEST_CASES,
                                                     FLOAT_TESTS_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     NO_HTML_TEST_CASES_SORT,
                                                     UTF8_TEST_CASES)


class TestMoveCreateCommon(BaseTestCase):
    """Test Move create Common"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateCommon, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_as_anonymous_is_forbidden(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        assert self.send_post(payload, code=401)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_bad_move_type(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(666, geokret=geokret)\
            .set_coordinates()
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/type')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_move_on_datetime_must_be_present(self, move_type):
        geokret = self.blend_geokret(created_on_datetime='2018-10-07T15:30:52')
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        del payload['data']['attributes']['moved-on-datetime']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_move_on_datetime_must_be_after_born_date(self, move_type):
        geokret = self.blend_geokret(created_on_datetime='2018-10-07T15:30:52')
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_moved_on_datetime('2018-10-07T10:00:00')
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

        payload.set_moved_on_datetime('2018-10-07T19:00:00')
        response = self.send_post(payload, user=self.user_1, code=201)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_move_on_datetime_must_not_be_in_the_future(self, move_type):
        geokret = self.blend_geokret(created_on_datetime='2018-10-07T15:30:52')
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_moved_on_datetime(datetime.now() + timedelta(hours=6))
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

        payload.set_moved_on_datetime(datetime.utcnow() - timedelta(hours=1))
        response = self.send_post(payload, user=self.user_1, code=201)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_move_on_datetime_must_not_be_at_the_same_datetime(self, move_type):
        geokret = self.blend_geokret(created_on_datetime='2018-10-07T15:30:52')
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_moved_on_datetime('2018-10-09T19:40:28')
        self.send_post(payload, user=self.user_1, code=201)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_comment_may_be_absent(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        del payload['data']['attributes']['comment']
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('comment', '')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_comment(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_comment('Some text')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('comment', 'Some text')

    @parameterized.expand(HTML_SUBSET_TEST_CASES)
    @request_context
    def test_move_create_field_comment_accept_html_subset(self, comment, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        payload.set_comment(comment)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('comment', expected)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_move_create_field_comment_accept_unicode(self, comment, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)
        payload.set_comment(comment)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('comment', expected)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_relationship_author_defaults_to_current_user(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['relationships'].pop('author', None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasRelationshipAuthorData(self.user_1.id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_relationship_author_is_not_overridable(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_author(self.user_2.id)
        response = self.send_post(payload, user=self.user_1, code=403)
        response.assertRaiseJsonApiError('/data/relationships/author')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_relationship_author_can_be_overrided_by_an_admin(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_author(self.user_2.id)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasRelationshipAuthorData(self.user_2.id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_name_may_be_absent(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('application_name', None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-name', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_name_may_be_none(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_application_name(None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-name', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_name(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_application_name('Some name')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-name', 'Some name')

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_move_create_field_application_name_no_html(self, application_name, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DIPPED, geokret=geokret)\
            .set_coordinates()
        payload.set_application_name(application_name)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-name', expected)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_version_may_be_absent(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('application_version', None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-version', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_version_may_be_none(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_application_version(None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-version', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_version(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_application_version('1.0.0')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-version', '1.0.0')

    @parameterized.expand(NO_HTML_TEST_CASES_SORT)
    @request_context
    def test_move_create_field_application_version_no_html(self, application_version, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DIPPED, geokret=geokret)\
            .set_coordinates()
        payload.set_application_version(application_version)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('application-version', expected)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_application_version_too_long(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_application_version('1.0.0.1.0.0.1.0.0.1.0.0.1.0.0')
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/application-version')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_comment_count_is_computed_and_not_overridable(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('comments-count', 666)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('comments-count', 0)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_picture_count_is_computed_and_not_overridable(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('pictures-count', 666)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('pictures-count', 0)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_altitude_is_computed_and_not_overridable_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('altitude', 666)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('altitude', 996)

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_altitude_computed_and_is_not_overridable_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('altitude', 666)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('altitude', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
        [MOVE_TYPE_GRABBED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_country_is_computed_and_not_overridable_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('country', 'pl')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('country', 'FR')

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_country_is_computed_and_not_overridable_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('country', 'pl')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('country', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_distance_is_computed_and_not_overridable(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('distance', 666)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('distance', 0)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_creation_datetime_set_automatically(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('created-on-datetime', None)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertCreationDateTime()

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_update_datetime_set_automatically(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('updated-on-datetime', None)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertUpdatedDateTime()

    @parameterized.expand([
        [u'ééééé'],
        [u'<'],
        [u'\x01 '],
        [u'";!'],
    ])
    @request_context
    def test_move_create_field_tracking_code_must_be_alphanumeric(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_tracking_code_must_be_present_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret).set_coordinates()
        del payload['data']['attributes']['tracking-code']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

        payload.set_tracking_code('')
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_move_create_field_tracking_code_cannot_be_blank_2(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret).set_coordinates()
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand([
        [u'ééééé'],
        [u'<'],
        [u'\x01 '],
        [u'";!'],
    ])
    @request_context
    def test_move_create_field_waypoint_must_be_alphanumeric(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/waypoint')

    @parameterized.expand(BLANK_CHARACTERS_TEST_CASES)
    @request_context
    def test_move_create_field_waypoint_dont_accept_blank_characters(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/waypoint')

    @parameterized.expand(FLOAT_TESTS_CASES)
    @request_context
    def test_move_create_field_latitude_must_be_decimal(self, latitude, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(latitude, 0.0)
        if expected == 201:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertHasAttribute('latitude', latitude)
        else:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand(FLOAT_TESTS_CASES)
    @request_context
    def test_move_create_field_longitude_must_be_decimal(self, longitude, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(0.0, longitude)
        if expected == 201:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertHasAttribute('longitude', longitude)
        else:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_latitude_mandatory_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('longitude', 6.2)
        del payload['data']['attributes']['latitude']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_latitude_mandatory_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('longitude', 6.2)
        del payload['data']['attributes']['latitude']
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)
        response.assertHasAttribute('longitude', None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_longitude_mandatory_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('latitude', 6.2)
        del payload['data']['attributes']['longitude']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_longitude_mandatory_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        payload._set_attribute('latitude', 6.2)
        del payload['data']['attributes']['longitude']
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)
        response.assertHasAttribute('longitude', None)

    @parameterized.expand([
        [MOVE_TYPE_COMMENT],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_longitude_mandatory_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertNotHasAttribute('latitude')
        response.assertNotHasAttribute('longitude')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_waypoint_1(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()\
            .set_waypoint('GC5BRQK')
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', 'GC5BRQK')

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_waypoint_2(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @parameterized.expand([
        [MOVE_TYPE_COMMENT],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_field_waypoint_3(self, move_type):
        geokret = self.blend_geokret()
        payload = MovePayload(move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertNotHasAttribute('waypoint')

    @parameterized.expand([
        [-180.0],
        [-91.0],
        [-90.1],
        [-90.001],
        [90.001],
        [90.1],
        [91.0],
        [180.0],
    ])
    @request_context
    def test_move_create_field_latitude_must_be_valid(self, latitude):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(latitude, 0.0)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand([
        [-250.0],
        [-181.0],
        [-180.1],
        [-180.001],
        [180.001],
        [180.1],
        [181.0],
        [250.0],
    ])
    @request_context
    def test_move_create_field_longitude_must_be_valid(self, longitude):
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(0.0, longitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_geokret_last_move_must_be_updated(self, move_type):
        geokret = self.blend_geokret()
        self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T21:26:16")
        payload = MovePayload(move_type, geokret=geokret)\
            .set_coordinates()
        response = self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.last_move_id, response.id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_geokret_last_position_must_be_updated_1(self, move_type):
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:37:10")
        self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:37:20")
        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:37:46")\
            .set_coordinates()
        # print geokret.created_on_datetime
        response = self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.last_position_id, response.id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_SEEN],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_geokret_last_position_must_be_updated_1_as_intermediate_move(self, move_type):
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:37:10")
        self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:37:20")
        move2 = self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:37:30")
        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:37:25")\
            .set_coordinates()
        # print geokret.created_on_datetime
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.last_position_id, move2.id)

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_geokret_last_position_must_be_updated_2(self, move_type):
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:37:10")
        move1 = self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                                geokret=geokret, moved_on_datetime="2018-10-19T22:37:20")
        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:37:46")\
            .set_coordinates()
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.last_position_id, move1.id)

    @parameterized.expand([
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_geokret_last_position_must_be_updated_2_as_intermediate_move(self, move_type):
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:37:10")
        self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                                geokret=geokret, moved_on_datetime="2018-10-19T22:37:20")
        move2 = self.blend_move(type=MOVE_TYPE_DROPPED, author=self.user_2,
                                geokret=geokret, moved_on_datetime="2018-10-19T22:37:40")
        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:37:30")\
            .set_coordinates()
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.last_position_id, move2.id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, None],
        [MOVE_TYPE_GRABBED, 'user_1'],
        [MOVE_TYPE_COMMENT, 'user_2'],
        [MOVE_TYPE_SEEN, None],
        [MOVE_TYPE_DIPPED, 'user_1'],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_grabbed_geokret_holder_must_be_updated(self, move_type, username):
        user_id = getattr(self, username).id if username else None
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:43:44")
        self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:44:00")

        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret, moved_on_datetime="2018-10-19T22:44:04")
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.holder_id, self.user_2.id)

        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:44:08").set_coordinates()
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.holder_id, user_id)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_move_create_grabbed_geokret_holder_must_be_updated_as_intermediate_move(self, move_type):
        geokret = self.blend_geokret(created_on_datetime="2018-10-19T22:49:42")
        self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:49:45")
        self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_2,
                        geokret=geokret, moved_on_datetime="2018-10-19T22:50:05")

        payload = MovePayload(move_type, geokret=geokret, moved_on_datetime="2018-10-19T22:50:00").set_coordinates()
        self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(geokret.holder_id, self.user_2.id)

    # TODO https://github.com/geokrety/geokrety-api/issues/96
    # @request_context
    # def test_move_create_dropped_geokret_missing_must_be_updated(self):
    #     geokret = self.blend_geokret(created_on_datetime="2018-10-19T19:50:29")
    #     geokret.missing = True
    #
    #     payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret, moved_on_datetime="2018-10-19T19:52:56")
    #     self.send_post(payload, user=self.user_1, code=201)
    #     self.assertFalse(geokret.missing)
