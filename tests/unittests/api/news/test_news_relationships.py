# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context


class TestNewsRelationships(BaseTestCase):
    """Test News relationships"""

    def validate(self, url, item_id):
        response = self._send_get(url.format(self.news.id), user=self.user_2).get_json()
        self.assertEqual(response['data']['id'], item_id)

    def validate_multiple(self, url, item_id):
        response = self._send_get(url.format(self.news.id), user=self.user_2).get_json()
        self.assertEqual(response['data'][0]['id'], item_id)

    @request_context
    def test_news_news_comments_relationship(self):
        self.news = self.blend_news(author=self.user_1)
        news_comment = self.blend_news_comment(news=self.news)
        url = "/v1/news/{}/relationships/news-comments"
        self.validate_multiple(url, news_comment.id)

    @request_context
    def test_news_author_relationship(self):
        self.news = self.blend_news(author=self.user_1)
        url = "/v1/news/{}/relationships/author"
        self.validate(url, self.user_1.id)

    @request_context
    def test_news_subscribed_users_relationship(self):
        self.news = self.blend_news(author=self.user_1)
        news_subscription = self.blend_news_subscription(news=self.news)
        url = "/v1/news/{}/relationships/subscriptions"
        self.validate_multiple(url, news_subscription.id)
