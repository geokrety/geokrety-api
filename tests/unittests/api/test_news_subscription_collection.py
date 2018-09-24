# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.collections import NewsSubscriptionCollectionResponse


class TestNewsSubscriptionCollection(BaseTestCase):
    """Test NewsSubscription collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-subscriptions?%s" % (args_)
        return NewsSubscriptionCollectionResponse(self._send_get(url, **kwargs).get_json())

    @request_context
    def test_news_subscription_collection_admin_can_list_all_subscriptions(self):
        self.blend_news_subscription(count=3)
        response = self.send_get(user=self.admin)
        response.assertCount(3)

    @request_context
    def test_news_subscription_collection_subscriber_can_list_his_subscriptions(self):
        self.blend_news_subscription(count=3)
        news_subscription = self.blend_news_subscription(user=self.user_1)
        response = self.send_get(user=self.user_1)
        response.assertCount(1)
        response.data[0].assertHasId(news_subscription.id)

    @request_context
    def test_news_subscription_collection_authenticated_cannot_list_others_subscriptions(self):
        self.blend_news_subscription(count=3)
        self.blend_news_subscription(user=self.user_1)
        response = self.send_get(user=self.user_2)
        response.assertCount(0)

    @request_context
    def test_news_subscription_collection_anonymous_cannot_list_any_subscriptions(self):
        self.blend_news_subscription(count=3)
        self.send_get(user=None, code=401)

    @request_context
    def test_news_subscription_collection_has_normal_attributes(self):
        news_subscription = self.blend_news_subscription()
        response = self.send_get(user=self.admin)
        response.assertCount(1)
        response.data[0].assertHasPublicAttributes(news_subscription)
