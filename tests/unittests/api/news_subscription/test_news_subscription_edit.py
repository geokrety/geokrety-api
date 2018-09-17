# -*- coding: utf-8 -*-

import urllib

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_subscription import \
    NewsSubscriptionPayload
from tests.unittests.utils.responses.collections import \
    NewsSubscriptionResponse


class TestNewsSubscriptionEdit(BaseTestCase):
    """Test NewsSubscription edit"""

    def send_patch(self, obj_id, payload, args=None, **kwargs):
        args = {'include': 'user,news'}
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-subscriptions/%s?%s" % (obj_id, args_)
        payload.set_id(obj_id)
        return NewsSubscriptionResponse(self._send_patch(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_news_subscription_edit_anonymous_cannot_edit_subscriptions(self):
        news_subscription = self.blend_news_subscription()
        payload = NewsSubscriptionPayload()
        self.send_patch(news_subscription.id, payload, user=None, code=401)

    @request_context
    def test_news_subscription_edit_user_can_edit_his_subscription_status(self):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        payload = NewsSubscriptionPayload()
        payload.set_subscribed(False)
        response = self.send_patch(news_subscription.id, payload, user=self.user_1)
        response.assertHasSubscribed(False)
        payload.set_subscribed(True)
        response = self.send_patch(news_subscription.id, payload, user=self.user_1)
        response.assertHasSubscribed(True)

    @request_context
    def test_news_subscription_edit_user_can_edit_his_subscription_news(self):
        news = self.blend_news()
        news_subscription = self.blend_news_subscription(user=self.user_1)
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        response = self.send_patch(news_subscription.id, payload, user=self.user_1)
        response.assertHasRelationshipNewsData(news.id)

    @request_context
    def test_news_subscription_edit_user_cannot_edit_subscriptions_for_others_status(self):
        news_subscription = self.blend_news_subscription(user=self.user_2)
        payload = NewsSubscriptionPayload()
        payload.set_subscribed(False)
        self.send_patch(news_subscription.id, payload, user=self.user_1, code=403)

    @request_context
    def test_news_subscription_edit_user_cannot_edit_subscriptions_for_others_news(self):
        news = self.blend_news()
        news_subscription = self.blend_news_subscription(user=self.user_2)
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        self.send_patch(news_subscription.id, payload, user=self.user_1, code=403)

    @request_context
    def test_news_subscription_edit_admin_can_edit_any_subscription_status(self):
        news_subscription = self.blend_news_subscription(user=self.user_1)
        payload = NewsSubscriptionPayload()
        payload.set_subscribed(False)
        response = self.send_patch(news_subscription.id, payload, user=self.admin)
        response.assertHasSubscribed(False)
        payload.set_subscribed(True)
        response = self.send_patch(news_subscription.id, payload, user=self.admin)
        response.assertHasSubscribed(True)

    @request_context
    def test_news_subscription_edit_admin_can_edit_any_subscription_news(self):
        news = self.blend_news()
        news_subscription = self.blend_news_subscription(user=self.user_1)
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        response = self.send_patch(news_subscription.id, payload, user=self.admin)
        response.assertHasRelationshipNewsData(news.id)

    @request_context
    def test_news_subscription_edit_field_subscribed_on_datetime_is_immuable(self):
        news_subscription = self.blend_news_subscription()
        payload = NewsSubscriptionPayload()
        payload._set_attribute('subscribed_on_datetime', "2018-09-25T22:02:58")
        response = self.send_patch(news_subscription.id, payload, user=self.admin)
        response.assertHasAttributeDateTime('subscribed_on_datetime', news_subscription.subscribed_on_datetime)
