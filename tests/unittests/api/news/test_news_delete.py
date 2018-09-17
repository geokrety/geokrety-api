# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.news import NewsResponse


class TestNewsDelete(BaseTestCase):
    """Test News delete"""

    def send_delete(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news/%s?%s" % (obj_id, args_)
        return NewsResponse(self._send_delete(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_news_delete_as(self, username, expected):
        news = self.blend_news()
        user = getattr(self, username) if username else None
        assert self.send_delete(news.id, user=user, code=expected)
