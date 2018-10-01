# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from app.models import db
from app.models.news_subscription import NewsSubscription
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_comment import NewsCommentPayload
from tests.unittests.utils.responses.news_comment import NewsCommentResponse


class TestNewsCommentDelete(BaseTestCase):
    """Test NewsComment delete"""

    def send_delete(self, id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-comments/%s?%s" % (id, args_)
        return NewsCommentResponse(self._send_delete(url, **kwargs).get_json())

    def send_post(self, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-comments?%s" % (args_)
        return NewsCommentResponse(self._send_post(url, payload=payload, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 200],
        ['user_2', 403],
    ])
    @request_context
    def test_news_comment_delete_as(self, input, expected):
        news = self.blend_news()
        news_comment = self.blend_news_comment(news=news, author=self.user_1)
        user = getattr(self, input) if input else None
        assert self.send_delete(news_comment.id, user=user, code=expected)

    @request_context
    def test_news_comment_delete_news_comments_counter_must_be_decremented(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_news(news.id)
        news_comment = self.send_post(payload=payload, user=self.admin)
        self.assertEqual(news.comments_count, 1)
        response = self.send_delete(news_comment.id, user=self.admin)
        self.assertEqual(news.comments_count, 0)

    @request_context
    def test_news_comment_delete_news_subscription_must_be_cleaned(self):
        news = self.blend_news()
        payload = NewsCommentPayload()
        payload.set_news(news.id)
        payload.set_subscribe(True)
        news_comment = self.send_post(payload=payload, user=self.admin)
        self.send_post(payload=payload, user=self.user_1)
        self.assertEqual(news.comments_count, 2)

        news_subscription = db.session \
            .query(NewsSubscription) \
            .filter(NewsSubscription.user_id == self.admin.id, NewsSubscription.news_id == news.id)
        self.assertEqual(news_subscription.count(), 1)
        self.assertTrue(news_subscription.first().subscribed)

        response = self.send_delete(news_comment.id, user=self.admin)
        self.assertEqual(news.comments_count, 1)
        self.assertEqual(news_subscription.count(), 0)
