# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.news import NewsResponse


class TestNewsDetailsLinks(BaseTestCase):
    """Test News details links"""

    def validate(self, url, pointer=None, **kwargs):
        response = NewsResponse(self._send_get(url, user=self.user_2, **kwargs).get_json())
        if kwargs.get('code') == 404:
            response.assertRaiseJsonApiError(pointer)
        else:
            response.assertHasPublicAttributes(self.news)

    @request_context
    def test_news_details_via_news_comment(self):
        self.news = self.blend_news()
        news_comment = self.blend_news_comment(news=self.news)
        url = "/v1/news-comments/{}/news".format(news_comment.id)
        self.validate(url)

    @request_context
    def test_news_details_via_news_comment_unexistent(self):
        url = "/v1/news-comments/{}/news".format(666)
        self.validate(url, code=404, pointer='news_comment_id')

    @request_context
    def test_news_details_via_news_subscriptions(self):
        self.news = self.blend_news()
        news_subscriptions = self.blend_news_subscription(user=self.user_2, news=self.news)
        url = "/v1/news-subscriptions/{}/news".format(news_subscriptions.id)
        self.validate(url)

    @request_context
    def test_news_details_via_news_subscriptions_unexistent(self):
        url = "/v1/news-subscriptions/{}/news".format(666)
        self.validate(url, code=404, pointer='news_subscription_id')
