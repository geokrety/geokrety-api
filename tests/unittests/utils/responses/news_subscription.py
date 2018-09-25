# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class NewsSubscriptionResponse(BaseResponse):

    @property
    def subscribed(self):
        return self.get_attribute('subscribed')

    @property
    def subscribed_on_datetime(self):
        return datetime.strptime(self.get_attribute('subscribed-on-datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def user(self):
        return self['relationships']['user']['data']['id']

    @property
    def news(self):
        return self['relationships']['news']['data']['id']

    def assertHasSubscribed(self, value):
        self.assertHasAttribute('subscribed', value)

    def assertHasRelationshipUser(self):
        self.assertHasRelationshipSelf('user', '/v1/news-subscriptions/%s/relationships/user' % self.id)
        self.assertHasRelationshipRelated('user', '/v1/news-subscriptions/%s/user' % self.id)

    def assertHasRelationshipNews(self):
        self.assertHasRelationshipSelf('news', '/v1/news-subscriptions/%s/relationships/news' % self.id)
        self.assertHasRelationshipRelated('news', '/v1/news-subscriptions/%s/news' % self.id)

    def assertHasRelationshipUserData(self, user_id):
        self.assertHasRelationshipData('user', user_id, 'user')

    def assertHasRelationshipNewsData(self, news_id):
        self.assertHasRelationshipData('news', news_id, 'news')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('subscribed', obj.subscribed)
        self.assertDateTimePresent('subscribed-on-datetime')
        self.assertHasAttributeDateTime('subscribed-on-datetime', obj.subscribed_on_datetime)
        self.assertHasRelationshipUser()
        self.assertHasRelationshipNews()
