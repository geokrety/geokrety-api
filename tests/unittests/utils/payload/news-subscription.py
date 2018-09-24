# -*- coding: utf-8 -*-

from mixer.backend.flask import mixer

from .base import BasePayload


class NewsSubscriptionPayload(BasePayload):
    def __init__(self):
        super(NewsSubscriptionPayload, self).__init__('news-subscription')

    def set_user(self, user_id):
        self._set_relationships('user', 'user', user_id)
        return self

    def set_news(self, news_id):
        self._set_relationships('news', 'news', news_id)
        return self

    def set_obj(self, obj):
        self.set_subscribed_on_datetime(obj.subscribed_on_datetime)
        self.set_subscribed(obj.subscribed)
        if obj.user.id:
            self.set_user(obj.user.id)
        if obj.news.id:
            self.set_news(obj.news.id)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend('app.models.news_subscription.NewsSubscription'))
            return self
