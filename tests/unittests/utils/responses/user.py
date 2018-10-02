# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class UserResponse(BaseResponse):

    @property
    def name(self):
        return self.get_attribute('name')

    @property
    def password(self):
        return self.get_attribute('password')

    @property
    def email(self):
        return self.get_attribute('email')

    @property
    def daily_mails(self):
        return self.get_attribute('daily_mails')

    @property
    def ip(self):
        return self.get_attribute('ip')

    @property
    def language(self):
        return self.get_attribute('language')

    @property
    def latitude(self):
        return self.get_attribute('latitude')

    @property
    def longitude(self):
        return self.get_attribute('longitude')

    @property
    def observation_radius(self):
        return self.get_attribute('observation_radius')

    @property
    def country(self):
        return self.get_attribute('country')

    @property
    def hour(self):
        return self.get_attribute('hour')

    @property
    def statpic_id(self):
        return self.get_attribute('statpic_id')

    @property
    def secid(self):
        return self.get_attribute('secid')

    @property
    def join_datetime(self):
        return datetime.strptime(self.get_attribute('join_datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def last_mail_datetime(self):
        return datetime.strptime(self.get_attribute('last_mail_datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def last_login_datetime(self):
        return datetime.strptime(self.get_attribute('last_login_datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def last_update_datetime(self):
        return datetime.strptime(self.get_attribute('last_login_datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def news(self):
        return self['relationships']['news']['data']['id']

    @property
    def news_comments(self):
        return self['relationships']['news-comments']['data']['id']

    @property
    def news_subscriptions(self):
        return self['relationships']['news-subscriptions']['data']['id']

    @property
    def negeokrety_ownedws(self):
        return self['relationships']['geokrety-owned']['data']['id']

    @property
    def geokrety_held(self):
        return self['relationships']['geokrety-held']['data']['id']

    @property
    def moves(self):
        return self['relationships']['moves']['data']['id']

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

    def assertHasRelationshipNewsData(self, user_id):
        self.assertHasRelationshipData('news', user_id, 'news')

    def assertHasRelationshipNewsCommentsData(self, user_id):
        self.assertHasRelationshipData('news_comments', user_id, 'news-comments')

    def assertHasRelationshipNewsSubscriptionsAuthorData(self, user_id):
        self.assertHasRelationshipData('news_subscriptions', user_id, 'news-subscriptions')

    def assertHasRelationshipGeokretyOwnedData(self, user_id):
        self.assertHasRelationshipData('geokrety_owned', user_id, 'geokrety-owned')

    def assertHasRelationshipGeokretyHeldData(self, user_id):
        self.assertHasRelationshipData('geokrety_held', user_id, 'geokrety-held')

    def assertHasRelationshipMovesData(self, user_id):
        self.assertHasRelationshipData('moves', user_id, 'moves')

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
