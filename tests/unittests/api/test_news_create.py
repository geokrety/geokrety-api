# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news import NewsPayload
from tests.unittests.utils.responses.news import NewsResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES_NO_BLANK,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestNewsCreate(BaseTestCase):
    """Test News create"""

    def send_post(self, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news?%s" % (args_)
        return NewsResponse(self._send_post(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_news_create_as_anonymous(self):
        payload = NewsPayload()
        assert self.send_post(payload, user=None, code=401)

    @request_context
    def test_news_create_as_authenticated(self):
        payload = NewsPayload()
        assert self.send_post(payload, user=self.user_1, code=403)

    @request_context
    def test_news_create_as_admin(self):
        payload = NewsPayload()
        assert self.send_post(payload, user=self.admin)

    @request_context
    def test_news_create_field_author_enforced_to_current_user(self):
        payload = NewsPayload()
        payload.set_author(self.user_1.id)
        response = self.send_post(payload, user=self.admin)
        response.assertHasRelationshipAuthorData(self.user_1.id)

    @request_context
    def test_news_create_field_author_enforced_to_current_user_if_undefined(self):
        payload = NewsPayload()
        payload.set_author('')
        response = self.send_post(payload, user=self.admin)
        response.assertHasRelationshipAuthorData(self.admin.id)

    @request_context
    def test_news_create_field_username_enforced_to_current_user_if_undefined(self):
        payload = NewsPayload()
        payload['data']['attributes'].pop('username', None)
        response = self.send_post(payload, user=self.admin)
        self.assertEqual(response.username, self.admin.name)

    @request_context
    def test_news_create_field_username_can_be_overrided(self):
        payload = NewsPayload()
        payload.set_username(self.user_1.name)
        response = self.send_post(payload, user=self.admin)
        self.assertEqual(response.username, self.user_1.name)

    @request_context
    def test_news_create_field_title_is_mandatory(self):
        payload = NewsPayload()
        payload['data']['attributes'].pop('title', None)
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/title')

    @request_context
    def test_news_create_field_content_is_mandatory(self):
        payload = NewsPayload()
        payload['data']['attributes'].pop('content', None)
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/content')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_news_create_field_title_cannot_be_blank(self, title):
        payload = NewsPayload()
        payload.set_title(title)
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/title')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_news_create_field_content_cannot_be_blank(self, content):
        payload = NewsPayload()
        payload.set_content(content)
        news = self.blend_news()
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/content')

    @request_context
    def test_news_create_field_creation_datetime_set_automatically(self):
        payload = NewsPayload()
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertCreationDateTime()

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_create_field_name_accept_unicode(self, title, result=None):
        payload = NewsPayload()
        payload.set_title(title)
        result = title if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('title', result)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_create_field_content_accept_unicode(self, content, result=None):
        payload = NewsPayload()
        payload.set_content(content)
        result = content if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('content', result)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_create_field_username_accept_unicode(self, username, result=None):
        payload = NewsPayload()
        payload.set_username(username)
        result = username if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('username', result)

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_news_create_field_title_doesnt_accept_html(self, title, result=None):
        payload = NewsPayload()
        payload.set_title(title)
        result = title if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('title', result)

    @parameterized.expand(HTML_SUBSET_TEST_CASES_NO_BLANK)
    @request_context
    def test_news_create_field_content_accept_html_subset(self, content, result=None):
        payload = NewsPayload()
        payload.set_content(content)
        result = content if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('content', result)

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_news_create_field_username_doesnt_accept_html(self, username, result=None):
        payload = NewsPayload()
        payload.set_username(username)
        result = username if result is None else result
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasAttribute('username', result)
