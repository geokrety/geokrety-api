# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.news_subscription import NewsSubscriptionResponse


class TestNewsSubscriptionDetails(BaseTestCase):
    """Test NewsSubscription details"""

    def send_get(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-subscriptions/%s?%s" % (obj_id, args_)
        return NewsSubscriptionResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 200],  # Owner
        ['user_2', 403],
    ])
    @request_context
    def test_news_subscription_details_can_be_accessed_as(self, username, expected):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        user = getattr(self, username) if username else None
        self.send_get(news_subscription.id, user=user, code=expected)

    @parameterized.expand([
        ['admin'],
        ['user_1'],  # Owner
    ])
    @request_context
    def test_news_subscription_details_has_normal_attributes_as(self, username):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        user = getattr(self, username)
        response = self.send_get(news_subscription.id, user=user)
        response.assertHasPublicAttributes(news_subscription)
