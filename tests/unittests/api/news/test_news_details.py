# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.news import NewsResponse


class TestNewsDetails(BaseTestCase):
    """Test News details"""

    def send_get(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news/%s?%s" % (obj_id, args_)
        return NewsResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [None],
        ['admin'],
        ['user_1'],  # Owner
        ['user_2'],
    ])
    @request_context
    def test_news_details_has_normal_attributes_as(self, username):
        news = self.blend_news(author=self.user_1)
        user = getattr(self, username) if username else None
        response = self.send_get(news.id, user=user)
        response.assertHasPublicAttributes(news)
