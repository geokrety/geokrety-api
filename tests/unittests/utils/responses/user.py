# -*- coding: utf-8 -*-

from base import BaseResponse


class UserResponse(BaseResponse):

    def assertHasRelationshipNews(self):
        self.assertHasRelationshipSelf('news', '/v1/users/%s/relationships/news' % self.id)
        self.assertHasRelationshipRelated('news', '/v1/users/%s/news' % self.id)

    def assertHasRelationshipNewsComments(self):
        self.assertHasRelationshipSelf('news_comments', '/v1/users/%s/relationships/news-comments' % self.id)
        self.assertHasRelationshipRelated('news_comments', '/v1/users/%s/news-comments' % self.id)

    def assertHasRelationshipNewsSubscriptions(self):
        self.assertHasRelationshipSelf('news_subscriptions', '/v1/users/%s/relationships/news-subscription' % self.id)
        self.assertHasRelationshipRelated('news_subscriptions', '/v1/users/%s/news-subscription' % self.id)

    def assertHasRelationshipGeokretyOwned(self):
        self.assertHasRelationshipSelf('geokrety_owned', '/v1/users/%s/relationships/geokrety-owned' % self.id)
        self.assertHasRelationshipRelated('geokrety_owned', '/v1/users/%s/geokrety-owned' % self.id)

    def assertHasRelationshipGeokretyHeld(self):
        self.assertHasRelationshipSelf('geokrety_held', '/v1/users/%s/relationships/geokrety-held' % self.id)
        self.assertHasRelationshipRelated('geokrety_held', '/v1/users/%s/geokrety-held' % self.id)

    def assertHasRelationshipMoves(self):
        self.assertHasRelationshipSelf('moves', '/v1/users/%s/relationships/moves' % self.id)
        self.assertHasRelationshipRelated('moves', '/v1/users/%s/moves' % self.id)

    def assertHasRelationshipNewsDatas(self, user_id):
        self.assertHasRelationshipDatas('news', user_id, 'news')

    def assertHasRelationshipNewsCommentsDatas(self, user_id):
        self.assertHasRelationshipDatas('news_comments', user_id, 'news-comment')

    def assertHasRelationshipNewsSubscriptionsAuthorDatas(self, user_id):
        self.assertHasRelationshipDatas('news_subscriptions', user_id, 'news-subscription')

    def assertHasRelationshipGeokretyOwnedDatas(self, user_id):
        self.assertHasRelationshipDatas('geokrety_owned', user_id, 'geokret')

    def assertHasRelationshipGeokretyHeldDatas(self, user_id):
        self.assertHasRelationshipDatas('geokrety_held', user_id, 'geokret')

    def assertHasRelationshipMovesDatas(self, user_id):
        self.assertHasRelationshipDatas('moves', user_id, 'move')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('language', obj.language)
        self.assertHasAttribute('country', obj.country)
        self.assertHasAttributeDateTime('join_datetime', obj.join_datetime)
        self.assertHasRelationshipNews()
        self.assertHasRelationshipNewsComments()
        self.assertHasRelationshipGeokretyOwned()
        self.assertHasRelationshipGeokretyHeld()
        self.assertHasRelationshipMoves()
        with self.assertRaises(AssertionError):
            self.get_attribute('email')
        with self.assertRaises(AssertionError):
            self.get_attribute('password')
        with self.assertRaises(AssertionError):
            self.get_attribute('latitude')
        with self.assertRaises(AssertionError):
            self.get_attribute('longitude')
        with self.assertRaises(AssertionError):
            self.get_attribute('daily_mails')
        with self.assertRaises(AssertionError):
            self.get_attribute('observation_radius')
        with self.assertRaises(AssertionError):
            self.get_attribute('hour')
        with self.assertRaises(AssertionError):
            self.get_attribute('secid')
        with self.assertRaises(AssertionError):
            self.get_attribute('statpic_id')
        with self.assertRaises(AssertionError):
            self.get_attribute('last_update_datetime')
        with self.assertRaises(AssertionError):
            self.get_attribute('last_mail_datetime')
        with self.assertRaises(AssertionError):
            self.get_attribute('last_login_datetime')

    def assertHasPrivateAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('language', obj.language)
        self.assertHasAttribute('country', obj.country)
        self.assertHasAttributeDateTime('join_datetime', obj.join_datetime)
        self.assertHasAttribute('email', obj.email)
        with self.assertRaises(AssertionError):
            self.assertHasAttribute('password', obj.password)
        self.assertHasAttribute('latitude', obj.latitude)
        self.assertHasAttribute('longitude', obj.longitude)
        self.assertHasAttribute('daily_mails', obj.daily_mails)
        self.assertHasAttribute('observation_radius', obj.observation_radius)
        self.assertHasAttribute('hour', obj.hour)
        self.assertHasAttribute('secid', obj.secid)
        self.assertHasAttribute('statpic_id', obj.statpic_id)
        self.assertHasAttributeDateTimeOrNone('last_update_datetime', obj.last_update_datetime)
        self.assertHasAttributeDateTimeOrNone('last_mail_datetime', obj.last_mail_datetime)
        self.assertHasAttributeDateTimeOrNone('last_login_datetime', obj.last_login_datetime)
        self.assertHasRelationshipNews()
        self.assertHasRelationshipNewsComments()
        self.assertHasRelationshipGeokretyOwned()
        self.assertHasRelationshipGeokretyHeld()
        self.assertHasRelationshipMoves()
        self.assertHasRelationshipNewsSubscriptions()
