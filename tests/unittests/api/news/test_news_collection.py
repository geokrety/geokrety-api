# -*- coding: utf-8 -*-

import urllib

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.collections import NewsCollectionResponse


class TestNewsCollection(BaseTestCase):
    """Test News collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news?%s" % (args_)
        return NewsCollectionResponse(self._send_get(url, **kwargs).get_json())

    @request_context
    def test_news_collection_has_normal_attributes_as_anonymous_user(self):
        news = self.blend_news(author=self.user_1, count=3)
        response = self.send_get()
        i = 0
        for news_response in response.data:
            news_response.assertHasPublicAttributes(news[i])
            i = i + 1
