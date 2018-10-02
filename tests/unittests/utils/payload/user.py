# -*- coding: utf-8 -*-

from mixer.backend.flask import mixer

from .base import BasePayload


class UserPayload(BasePayload):
    def __init__(self):
        super(UserPayload, self).__init__('news')

    def set_name(self, name):
        self._set_attribute('name', name)
        return self

    def set_is_admin(self, is_admin):
        self._set_attribute('is_admin', is_admin)
        return self

    def set_password(self, password):
        self._set_attribute('password', password)
        return self

    def set_email(self, email):
        self._set_attribute('email', email)
        return self

    def set_daily_mails(self, daily_mails):
        self._set_attribute('daily_mails', daily_mails)
        return self

    def set_ip(self, ip):
        self._set_attribute('ip', ip)
        return self

    def set_language(self, language):
        self._set_attribute('language', language)
        return self

    def set_latitude(self, latitude):
        self._set_attribute('latitude', latitude)
        return self

    def set_longitude(self, longitude):
        self._set_attribute('longitude', longitude)
        return self

    def set_observation_radius(self, observation_radius):
        self._set_attribute('observation_radius', observation_radius)
        return self

    def set_country(self, country):
        self._set_attribute('country', country)
        return self

    def set_hour(self, hour):
        self._set_attribute('hour', hour)
        return self

    def set_statpic_id(self, statpic_id):
        self._set_attribute('statpic_id', statpic_id)
        return self

    def set_join_datetime(self, join_datetime):
        self._set_attribute('join_datetime', join_datetime)
        return self

    def set_last_mail_datetime(self, last_mail_datetime):
        self._set_attribute('last_mail_datetime', last_mail_datetime)
        return self

    def set_last_login_datetime(self, last_login_datetime):
        self._set_attribute('last_login_datetime', last_login_datetime)
        return self

    def set_last_update_datetime(self, last_update_datetime):
        self._set_attribute('last_update_datetime', last_update_datetime)
        return self

    def set_secid(self, secid):
        self._set_attribute('secid', secid)
        return self

    def set_news(self, news_id):
        self._set_relationships('news', 'news', news_id)
        return self

    def set_news_comments(self, news_comment_id):
        self._set_relationships('news-comments', 'comment', news_comment_id)
        return self

    def set_news_subscriptions(self, news_subscription_id):
        self._set_relationships('news-subscriptions', 'subscription', news_subscription_id)
        return self

    def set_geokrety_owned(self, geokrety_owned_ids):
        self._set_relationships('geokrety-owned', 'geokret', geokrety_owned_ids)
        return self

    def set_geokrety_held(self, geokrety_held_ids):
        self._set_relationships('geokrety-held', 'geokret', geokrety_held_ids)
        return self

    def set_moves(self, moves_ids):
        self._set_relationships('moves', 'geokret', moves_ids)
        return self

    def set_obj(self, obj):
        self.set_name(obj.title)
        self.set_is_admin(obj.title)
        self.set_password(obj.title)
        self.set_email(obj.title)
        self.set_daily_mails(obj.title)
        self.set_ip(obj.title)
        self.set_language(obj.title)
        self.set_latitude(obj.title)
        self.set_longitude(obj.title)
        self.set_observation_radius(obj.title)
        self.set_country(obj.title)
        self.set_hour(obj.title)
        self.set_statpic_id(obj.title)
        self.set_join_datetime(obj.title)
        self.set_last_mail_datetime(obj.title)
        self.set_last_login_datetime(obj.title)
        self.set_last_update_datetime(obj.title)
        self.set_secid(obj.title)
        if obj.news.id:
            self.set_news(obj.news.id)
        if obj.news_comments.id:
            self.set_news_comments(obj.news_comments.id)
        if obj.news_subscriptions.id:
            self.set_news_subscriptions(obj.news_subscriptions.id)
        if obj.geokrety_owned.id:
            self.set_geokrety_owned(obj.geokrety_owned.id)
        if obj.geokrety_held.id:
            self.set_geokrety_held(obj.geokrety_held.id)
        if obj.moves.id:
            self.set_moves(obj.moves.id)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend('app.models.user.User'))
            return self
