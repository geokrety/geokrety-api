# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context


class TestNewsCommentRelationships(BaseTestCase):
    """Test News Comment relationships"""

    def validate(self, url, item_id):
        response = self._send_get(url.format(self.news_comment.id), user=self.user_2).get_json()
        self.assertEqual(response['data']['id'], item_id)

    @request_context
    def test_news_comment_author_relationship(self):
        self.news_comment = self.blend_news_comment(author=self.user_1)
        url = "/v1/news-comments/{}/relationships/author"
        self.validate(url, self.user_1.id)

    @request_context
    def test_news_comment_move_relationship(self):
        news = self.blend_news()
        self.news_comment = self.blend_news_comment(news=news, author=self.user_1)
        url = "/v1/news-comments/{}/relationships/news"
        self.validate(url, news.id)
