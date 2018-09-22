# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.collections import NewsCollectionResponse


class TestNewsDetails(BaseTestCase):
    """Test News details"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news?%s" % (args_)
        return NewsCollectionResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],  # Owner
        ['user_2'],
    ])
    @request_context
    def test_news_details_has_normal_attributes_as_anonymous_user(self, input):
        news = self.blend_news(author=self.user_1, count=3)
        response = self.send_get()
        i = 0
        for news_response in response.data:
            news_response.assertHasPublicAttributes(news[i])
            i = i + 1
