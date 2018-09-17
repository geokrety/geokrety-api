# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.collections import NewsCommentCollectionResponse


class TestNewsCommentLinks(BaseTestCase):
    """Test News Comment links"""

    def validate(self, url, pointer=None, **kwargs):
        response = NewsCommentCollectionResponse(self._send_get(url, user=self.user_2, **kwargs).get_json())
        if kwargs.get('code') == 404:
            response.assertRaiseJsonApiError(pointer)
        else:
            response.data[0].assertHasPublicAttributes(self.news_comment)

    @request_context
    def test_news_comment_via_news(self):
        news = self.blend_news()
        self.news_comment = self.blend_news_comment(news=news)
        url = "/v1/news/{}/news-comments".format(news.id)
        self.validate(url)

    @request_context
    def test_news_comment_via_news_unexistent(self):
        url = "/v1/news/{}/news-comments".format(666)
        self.validate(url, code=404, pointer='news_id')

    @request_context
    def test_news_comment_via_author(self):
        self.news_comment = self.blend_news_comment(author=self.user_1)
        url = "/v1/users/{}/news-comments".format(self.user_1.id)
        self.validate(url)

    @request_context
    def test_news_comment_via_author_unexistent(self):
        url = "/v1/users/{}/news-comments".format(666)
        self.validate(url, code=404, pointer='author_id')
