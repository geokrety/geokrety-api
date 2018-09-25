# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_subscription import \
    NewsSubscriptionPayload
from tests.unittests.utils.responses.news_subscription import \
    NewsSubscriptionResponse


class TestNewsSubscriptionDelete(BaseTestCase):
    """Test NewsSubscription delete"""

    def send_delete(self, id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-subscriptions/%s?%s" % (id, args_)
        return NewsSubscriptionResponse(self._send_delete(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 200],
        ['user_2', 403],
    ])
    @request_context
    def test_news_subscription_delete_as(self, input, expected):
        news = self.blend_news_subscription(user=self.user_1)
        user = getattr(self, input) if input else None
        assert self.send_delete(news.id, user=user, code=expected)
