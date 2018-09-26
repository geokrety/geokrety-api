# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.news_comment import NewsCommentResponse


class TestNewsCommentDetails(BaseTestCase):
    """Test NewsComment details"""

    def send_get(self, id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-comments/%s?%s" % (id, args_)
        return NewsCommentResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 200],
        ['admin', 200],
        ['user_1', 200],  # Owner
        ['user_2', 200],
    ])
    @request_context
    def test_news_comment_details_can_be_accessed_as(self, input, expected):
        news_comment = self.blend_news_comment(user=self.user_1)
        user = getattr(self, input) if input else None
        response = self.send_get(news_comment.id, user=user, code=expected)
        response.assertHasPublicAttributes(news_comment)
