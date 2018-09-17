# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context


class TestUsersRelationships(BaseTestCase):
    """Test Users relationships"""

    def validate(self, url, item_id):
        response = self._send_get(url.format(self.user_1.id), user=self.user_2).get_json()
        self.assertEqual(response['data'][0]['id'], item_id)

    @request_context
    def test_user_move_relationship(self):
        move = self.blend_move(author=self.user_1)
        url = "/v1/users/{}/relationships/moves"
        self.validate(url, move.id)

    @request_context
    def test_user_news_relationship(self):
        news = self.blend_news(author=self.user_1)
        url = "/v1/users/{}/relationships/news"
        self.validate(url, news.id)

    @request_context
    def test_user_news_comments_relationship(self):
        news_comment = self.blend_news_comment(author=self.user_1)
        url = "/v1/users/{}/relationships/news-comments"
        self.validate(url, news_comment.id)

    @request_context
    def test_user_news_subscriptions_relationship(self):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        url = "/v1/users/{}/relationships/news-subscriptions"
        self.validate(url, news_subscription.id)

    @request_context
    def test_user_geokrety_owned_relationship(self):
        geokret = self.blend_geokret(owner=self.user_1)
        url = "/v1/users/{}/relationships/geokrety-owned"
        self.validate(url, geokret.id)

    @request_context
    def test_user_geokrety_held_relationship(self):
        geokret = self.blend_geokret(holder=self.user_1)
        url = "/v1/users/{}/relationships/geokrety-held"
        self.validate(url, geokret.id)
