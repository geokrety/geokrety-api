# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.user import UserResponse


class TestUsersDetailsLinks(BaseTestCase):
    """Test Users details links"""

    def validate(self, url, pointer=None, **kwargs):
        response = UserResponse(self._send_get(url, user=self.user_2, **kwargs).get_json())
        if kwargs.get('code') == 404:
            response.assertRaiseJsonApiError(pointer)
        else:
            response.assertHasPublicAttributes(self.user_1)

    @request_context
    def test_user_details_via_news_author(self):
        news = self.blend_news(author=self.user_1)
        url = "/v1/news/{}/author".format(news.id)
        self.validate(url)

    @request_context
    def test_user_details_via_news_author_unexistent(self):
        url = "/v1/news/{}/author".format(666)
        self.validate(url, code=404, pointer='news_author_id')

    @request_context
    def test_user_details_via_news_comment_author(self):
        news_comment = self.blend_news_comment(author=self.user_1)
        url = "/v1/news-comments/{}/author".format(news_comment.id)
        self.validate(url)

    @request_context
    def test_user_details_via_news_subscription(self):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        url = "/v1/news-subscriptions/{}/user".format(news_subscription.id)
        self.validate(url)

    @request_context
    def test_user_details_via_geokret_owner(self):
        geokret = self.blend_geokret(owner=self.user_1)
        url = "/v1/geokrety/{}/owner".format(geokret.id)
        self.validate(url)

    @request_context
    def test_user_details_via_geokret_holder(self):
        geokret = self.blend_geokret(holder=self.user_1)
        url = "/v1/geokrety/{}/holder".format(geokret.id)
        self.validate(url)

    @request_context
    def test_user_details_via_move_author(self):
        move = self.blend_move(author=self.user_1)
        url = "/v1/moves/{}/author".format(move.id)
        self.validate(url)
