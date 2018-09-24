# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_subscription import \
    NewsSubscriptionPayload
from tests.unittests.utils.responses.collections import \
    NewsSubscriptionResponse


class TestNewsSubscription(BaseTestCase):
    """Test NewsSubscription create"""

    def send_post(self, payload, args=None, **kwargs):
        if args is None:
            args = {'include': 'user,news'}
        else:
            args.update({'include': 'user,news'})
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-subscriptions?%s" % (args_)
        return NewsSubscriptionResponse(self._send_post(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_news_subscription_create_anonymous_cannot_subscribe(self):
        payload = NewsSubscriptionPayload()
        self.send_post(payload, user=None, code=401)

    @request_context
    def test_news_subscription_create_field_news_is_mandatory(self):
        payload = NewsSubscriptionPayload()
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/relationships/news/data')

    @request_context
    def test_news_subscription_create_field_user_is_current_user_by_default(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.user_1)
        response.assertHasRelationshipUserData(self.user_1.id)

    @request_context
    def test_news_subscription_create_field_subscribed_on_datetime_cannot_be_overrided(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        payload._set_attribute('subscribed_on_datetime', "2018-09-24T23:57:37")
        response = self.send_post(payload, user=self.user_1)
        with self.assertRaises(AssertionError):
            response.assertHasAttributeDateTime('subscribed-on-datetime', "2018-09-24T23:57:37")

    @request_context
    def test_news_subscription_create_authenticated_can_subscribe(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        payload.set_user(self.user_1.id)
        response = self.send_post(payload, user=self.user_1)
        response.assertHasAttribute('subscribed', True)
        response.assertHasRelationshipUserData(self.user_1.id)
        response.assertHasRelationshipNewsData(news.id)

    @request_context
    def test_news_subscription_create_authenticated_cannot_subscribe_someone_else(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        payload.set_user(self.user_2.id)
        response = self.send_post(payload, user=self.user_1, code=403)

    @request_context
    def test_news_subscription_create_admin_can_subscribe_someone_else(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        payload.set_user(self.user_1.id)
        response = self.send_post(payload, user=self.admin, code=201)
        response.assertHasRelationshipUserData(self.user_1.id)

    @request_context
    def test_news_subscription_create_unknown_news_raise_error(self):
        payload = NewsSubscriptionPayload()
        payload.set_news(666)
        self.send_post(payload, user=self.admin, code=404)

    @request_context
    def test_news_subscription_create_unknown_user_raise_error(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_news(news.id)
        payload.set_user(666)
        self.send_post(payload, user=self.admin, code=404)

    @request_context
    def test_news_subscription_create_field_subscribed_as_false_raise_error(self):
        news = self.blend_news()
        payload = NewsSubscriptionPayload()
        payload.set_subscribed(False)
        payload.set_news(news.id)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/subscribed')
