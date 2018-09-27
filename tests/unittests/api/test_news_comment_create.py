# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from app.api.helpers.db import safe_query
from app.models import db
from app.models.news_subscription import NewsSubscription
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_comment import NewsCommentPayload
from tests.unittests.utils.responses.news_comment import NewsCommentResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES_NO_BLANK,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestNewsCommentCreate(BaseTestCase):
    """Test NewsComment create"""

    def send_post(self, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-comments?%s" % (args_)
        return NewsCommentResponse(self._send_post(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_news_comment_create_can_be_posted_as_anonymous(self):
        response = self.send_post({}, user=None, code=401)

    @parameterized.expand([
        ['admin', 201],
        ['user_1', 201],
        ['user_2', 201],
    ])
    @request_context
    def test_news_comment_create_can_be_posted_as(self, input, expected):
        user = getattr(self, input) if input else None
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(user.id)
        payload.set_news(news.id)
        response = self.send_post(payload, user=user, code=expected)

    @request_context
    def test_news_comment_create_field_author_defaults_to_current_user(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasRelationshipAuthorData(self.user_1.id)

    @request_context
    def test_news_comment_create_field_author_defaults_to_current_user_even_for_admin(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasRelationshipAuthorData(self.admin.id)

    @request_context
    def test_news_comment_create_field_author_must_be_current_user(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_2.id)
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.user_1, code=403)
        response.assertRaiseJsonApiError('/data/relationships/author/data')

    @request_context
    def test_news_comment_create_field_author_can_be_overrided_by_admin(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_2.id)
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasRelationshipAuthorData(self.user_2.id)

    @request_context
    def test_news_comment_create_field_creation_datetime_set_automatically(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertCreationDateTime()

    @request_context
    def test_news_comment_create_field_comment_must_be_present(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload['data']['attributes'].pop('comment', None)
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/comment')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_news_comment_create_field_comment_cannot_be_blank(self, comment):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload.set_comment(comment)
        response = self.send_post(payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/comment')

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_comment_create_field_comment_must_accept_unicode(self, comment, expected=None):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload.set_comment(comment)
        expected = comment if expected is None else expected
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasComment(expected)

    @parameterized.expand(HTML_SUBSET_TEST_CASES_NO_BLANK)
    @request_context
    def test_news_comment_create_field_comment_must_accept_html_subset(self, comment, expected):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload.set_comment(comment)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasComment(expected)

    @request_context
    def test_news_comment_create_field_author_must_be_current_user(self):
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(666)
        self.send_post(payload, user=self.user_1, code=404)

    @request_context
    def test_news_comment_create_user_opted_in_to_subscribe_to_the_news(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload.set_subscribe(True)
        response = self.send_post(payload, user=self.user_1, code=201)
        assert 'subscribe' not in response['attributes']
        news_subscription = db.session \
            .query(NewsSubscription) \
            .filter(NewsSubscription.user_id == self.user_1.id, NewsSubscription.news_id == news.id)
        self.assertEqual(news_subscription.count(), 1)
        self.assertTrue(news_subscription.first().subscribed)

    @request_context
    def test_news_comment_create_user_did_not_opted_in_to_subscribe_to_the_news(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_author(self.user_1.id)
        payload.set_news(news.id)
        payload.set_subscribe(False)
        response = self.send_post(payload, user=self.user_1, code=201)
        assert 'subscribe' not in response['attributes']
        news_subscription = db.session \
            .query(NewsSubscription) \
            .filter(NewsSubscription.user_id == self.user_1.id, NewsSubscription.news_id == news.id)
        self.assertEqual(news_subscription.count(), 0)

    @request_context
    def test_news_comment_create_news_comments_counter_must_be_incremented(self):
        news = self.blend_news()
        self.assertEqual(news.comments_count, 0)
        payload = NewsCommentPayload()
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.user_1, code=201)
        self.assertEqual(news.comments_count, 1)
