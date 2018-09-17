# -*- coding: utf-8 -*-

import urllib

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.user import UserResponse


class TestUsersDetails(BaseTestCase):
    """Test Users details"""

    def send_get(self, obj_id, args=None, **kwargs):
        args = {'include': 'news,news_comments,news_subscriptions,geokrety_owned,geokrety_held,moves'}
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/users/%s?%s" % (obj_id, args_)
        return UserResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    @request_context
    def test_user_details_has_public_attributes_as_anonymous_user(self):
        response = self.send_get(self.user_1.id)
        response.assertHasPublicAttributes(self.user_1)

    @request_context
    def test_user_details_has_public_attributes_as_authenticated_user(self):
        response = self.send_get(self.user_1.id, user=self.user_2)
        response.assertHasPublicAttributes(self.user_1)

    @request_context
    def test_user_details_has_private_attributes_as_himself(self):
        response = self.send_get(self.user_1.id, user=self.user_1)
        response.assertHasPrivateAttributes(self.user_1)

    @request_context
    def test_user_details_has_private_attributes_as_admin(self):
        response = self.send_get(self.user_1.id, user=self.admin)
        response.assertHasPrivateAttributes(self.user_1)

    @request_context
    def test_user_details_has_relationships_data(self):
        news = self.blend_news(author=self.user_1, count=2)
        news_comments = self.blend_news_comment(author=self.user_1, count=2)
        news_subscriptions = self.blend_news_subscription(user=self.user_1, count=2)
        geokrety_owned = self.blend_geokret(owner=self.user_1, count=2)
        geokrety_held = self.blend_geokret(holder=self.user_1, count=2)
        moves = self.blend_move(author=self.user_1, count=2)
        response = self.send_get(self.user_1.id, user=self.admin)
        response.assertHasRelationshipNewsDatas(news)
        response.assertHasRelationshipNewsCommentsDatas(news_comments)
        response.assertHasRelationshipNewsSubscriptionsAuthorDatas(news_subscriptions)
        response.assertHasRelationshipGeokretyOwnedDatas(geokrety_owned)
        response.assertHasRelationshipGeokretyHeldDatas(geokrety_held)
        response.assertHasRelationshipMovesDatas(moves)
