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
from tests.unittests.utils.static_test_cases import (HTML_SUBSET_TEST_CASES,
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
