# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.models import db
from app.models.news_subscription import NewsSubscription
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.news_comment import NewsCommentPayload
from tests.unittests.utils.responses.news_comment import NewsCommentResponse
from tests.unittests.utils.static_test_cases import (HTML_SUBSET_TEST_CASES_NO_BLANK,
                                                     UTF8_TEST_CASES)


class TestNewsCommentEdit(BaseTestCase):
    """Test NewsComment edit"""

    def send_patch(self, obj_id, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/news-comments/%s?%s" % (obj_id, args_)
        payload.set_id(obj_id)
        return NewsCommentResponse(self._send_patch(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_news_comment_edit_authentication_required(self):
        news_comment = self.blend_news_comment()
        self.send_patch(news_comment.id, NewsCommentPayload(), user=None, code=401)

    @parameterized.expand([
        ['user_1', 200],
        ['user_2', 403],
    ])
    @request_context
    def test_news_comment_edit_author_can_edit_his_comments(self, username, expected):
        user = getattr(self, username) if username else None
        news_comment = self.blend_news_comment(author=self.user_1)
        payload = NewsCommentPayload()
        payload.set_comment('New text comment')
        response = self.send_patch(news_comment.id, payload, user=user, code=expected)
        if expected == 200:
            response.assertHasComment('New text comment')

    @request_context
    def test_news_comment_edit_admin_can_edit_any_comments(self):
        news_comment = self.blend_news_comment(author=self.user_1)
        payload = NewsCommentPayload()
        payload.set_comment('New text comment')
        response = self.send_patch(news_comment.id, payload, user=self.admin)
        response.assertHasComment('New text comment')

    @parameterized.expand(HTML_SUBSET_TEST_CASES_NO_BLANK)
    @request_context
    def test_news_comment_edit_field_comment_cannot_be_blank(self, comment, expected):
        news_comment = self.blend_news_comment()
        payload = NewsCommentPayload()
        payload.set_comment(comment)
        response = self.send_patch(news_comment.id, payload, user=self.admin)
        response.assertHasComment(expected)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_news_comment_edit_field_comment_must_accept_unicode(self, comment, expected):
        news_comment = self.blend_news_comment()
        payload = NewsCommentPayload()
        payload.set_comment(comment)
        response = self.send_patch(news_comment.id, payload, user=self.admin)
        response.assertHasComment(expected)

    @request_context
    def test_news_comment_edit_field_author_cannot_be_edited_by_users(self):
        news_comment = self.blend_news_comment(author=self.user_1)
        payload = NewsCommentPayload()
        payload.set_author(self.user_2.id)
        response = self.send_patch(news_comment.id, payload, user=self.user_1, code=403)
        response.assertRaiseJsonApiError('/data/relationships/author/data')

    @request_context
    def test_news_comment_edit_field_author_can_be_edited_by_admin(self):
        news_comment = self.blend_news_comment(author=self.user_1)
        payload = NewsCommentPayload()
        payload.set_author(self.user_2.id)
        response = self.send_patch(news_comment.id, payload, user=self.admin)
        response.assertHasRelationshipAuthorData(self.user_2.id)

    @request_context
    def test_news_comment_edit_field_creation_date_time_cannot_be_changed(self):
        news_comment = self.blend_news_comment()
        payload = NewsCommentPayload()
        payload._set_attribute('created_on_datetime', "2018-09-27T23:14:19")
        response = self.send_patch(news_comment.id, payload, user=self.admin)
        self.assertEqual(response.created_on_datetime, news_comment.created_on_datetime)

    @request_context
    def test_news_comment_edit_user_opted_in_to_subscribe_to_the_news(self):
        news_comment = self.blend_news_comment(author=self.user_1, subscribe=False)
        news_subscription = db.session \
            .query(NewsSubscription) \
            .filter(NewsSubscription.user_id == self.user_1.id, NewsSubscription.news_id == news_comment.news.id)
        self.assertEqual(news_subscription.count(), 0)

        payload = NewsCommentPayload()
        payload.set_subscribe(True)
        self.send_patch(news_comment.id, payload, user=self.user_1)
        self.assertEqual(news_subscription.count(), 1)

        payload = NewsCommentPayload()
        payload.set_subscribe(False)
        self.send_patch(news_comment.id, payload, user=self.user_1)
        self.assertEqual(news_subscription.count(), 0)
        # delete again
        self.send_patch(news_comment.id, payload, user=self.user_1)
        self.assertEqual(news_subscription.count(), 0)
