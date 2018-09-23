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


class TestNewsEdit(BaseTestCase):
    """Test News edit"""

    def send_patch(self, id, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news/%s?%s" % (id, args_)
        payload.set_id(id)
        return NewsResponse(self._send_patch(url, payload=payload, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_news_edit_as(self, input, expected):
        payload = NewsPayload()
        news = self.blend_news()
        user = getattr(self, input) if input else None
        assert self.send_patch(news.id, payload=payload, user=user, code=expected)

    @request_context
    def test_news_edit_field_title_can_be_edited(self):
        payload = NewsPayload()
        payload.set_title("New title")
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('title', "New title")

    @request_context
    def test_news_edit_field_content_can_be_edited(self):
        payload = NewsPayload()
        payload.set_content("New content")
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('content', "New content")

    @request_context
    def test_news_edit_field_username_can_be_edited(self):
        payload = NewsPayload()
        payload.set_username("New username")
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('username', "New username")

    @request_context
    def test_news_edit_field_author_can_be_edited(self):
        payload = NewsPayload()
        payload.set_author(self.user_1.id)
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasRelationshipAuthorData(self.user_1.id)

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_news_edit_field_title_cannot_be_blank(self, title):
        payload = NewsPayload()
        payload.set_title(title)
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/title')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_news_edit_field_content_cannot_be_blank(self, content):
        payload = NewsPayload()
        payload.set_content(content)
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/title')

    @request_context
    def test_news_edit_field_username_defaults_to_connected_username(self):
        payload = NewsPayload()
        payload.set_username('')
        news = self.blend_news()
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('username', self.admin.name)

    @request_context
    def test_geokret_patch_field_dump_only(self):
        payload = NewsPayload()
        payload._set_attribute('comments_count', 1000)
        payload._set_attribute('last_comment_date_time', "2018-09-23T23:13:36")
        payload._set_attribute('created_on_datetime', "2018-09-23T23:13:37")
        news = self.blend_news(
            comments_count=12,
            last_comment_date_time="2018-09-23T23:15:13",
            created_on_datetime="2018-09-23T23:15:14",
        )
        response = self.send_patch(news.id, payload, user=self.admin, code=200)
        self.assertEqual(response.comments_count, news.comments_count)
        self.assertEqual(response.last_comment_date_time, news.last_comment_date_time)
        self.assertEqual(response.created_on_datetime, news.created_on_datetime)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_edit_field_name_accept_unicode(self, title, result=None):
        payload = NewsPayload()
        payload.set_title(title)
        news = self.blend_news()
        result = title if result is None else result
        response = self.send_patch(news.id, payload, user=self.admin, code=200)
        response.assertHasAttribute('title', result)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_edit_field_content_accept_unicode(self, content, result=None):
        payload = NewsPayload()
        payload.set_content(content)
        news = self.blend_news()
        result = content if result is None else result
        response = self.send_patch(news.id, payload, user=self.admin, code=200)
        response.assertHasAttribute('content', result)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_edit_field_username_accept_unicode(self, username, result=None):
        payload = NewsPayload()
        payload.set_username(username)
        news = self.blend_news()
        result = username if result is None else result
        response = self.send_patch(news.id, payload, user=self.admin, code=200)
        response.assertHasAttribute('username', result)

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_news_edit_field_title_doesnt_accept_html(self, title, result=None):
        payload = NewsPayload()
        payload.set_title(title)
        news = self.blend_news()
        result = title if result is None else result
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('title', result)

    @parameterized.expand(HTML_SUBSET_TEST_CASES_NO_BLANK)
    @request_context
    def test_news_edit_field_content_accept_html_subset(self, content, result=None):
        payload = NewsPayload()
        payload.set_content(content)
        news = self.blend_news()
        result = content if result is None else result
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('content', result)

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_news_edit_field_username_doesnt_accept_html(self, username, result=None):
        payload = NewsPayload()
        payload.set_username(username)
        news = self.blend_news()
        result = username if result is None else result
        response = self.send_patch(news.id, payload=payload, user=self.admin, code=200)
        response.assertHasAttribute('username', result)
