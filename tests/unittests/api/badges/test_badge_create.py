# -*- coding: utf-8 -*-

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.badge import BadgePayload
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES_NO_BLANK,
                                                     UTF8_TEST_CASES)


class TestBadgeCreate(BaseTestCase):
    """Test badge create"""

    @parameterized.expand([
        [None, 401],
        ['admin', 201],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_only_administrator_can_create_badges(self, username, expected):
        user = getattr(self, username) if username else None
        BadgePayload()\
            .blend()\
            .post(user=user, code=expected)

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_field_name_cannot_be_empty(self, name):
        BadgePayload()\
            .blend()\
            .set_name(name)\
            .post(user=self.admin, code=422)\
            .assertRaiseJsonApiError('/data/attributes/name')

    @parameterized.expand(HTML_SUBSET_TEST_CASES_NO_BLANK)
    @request_context
    def test_field_name_support_html_subset(self, name, expected):
        BadgePayload()\
            .blend()\
            .set_name(name)\
            .post(user=self.admin)\
            .assertHasName(expected)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_field_name_support_utf8(self, name, expected):
        BadgePayload()\
            .blend()\
            .set_name(name)\
            .post(user=self.admin)\
            .assertHasName(expected)

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_field_description_can_be_empty(self, description):
        BadgePayload()\
            .blend()\
            .set_description(description)\
            .post(user=self.admin)\
            .assertHasDescription("")

    @parameterized.expand(HTML_SUBSET_TEST_CASES)
    @request_context
    def test_field_description_support_html_subset(self, description, expected):
        BadgePayload()\
            .blend()\
            .set_description(description)\
            .post(user=self.admin)\
            .assertHasDescription(expected)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_field_description_support_utf8(self, description, expected):
        BadgePayload()\
            .blend()\
            .set_description(description)\
            .post(user=self.admin)\
            .assertHasDescription(expected)

    @request_context
    def test_relationships_author_can_be_overrided(self):
        BadgePayload()\
            .blend()\
            .set_author(self.user_2)\
            .post(user=self.admin)\
            .assertHasRelationshipAuthorData(self.user_2.id)

    @request_context
    def test_relationships_author_is_optionnal(self):
        BadgePayload()\
            .blend()\
            ._del_relationships('author')\
            .post(user=self.admin)\
            .assertHasRelationshipAuthorData(self.admin)

    @request_context
    def test_field_filename_is_readonly(self):
        response = BadgePayload()\
            .blend()\
            .set_filename("filename")\
            .post(user=self.admin)

        self.assertIsNotNone(response.filename)
        self.assertNotEqual("", response.filename)
        self.assertNotEqual("filename", response.filename)
