# -*- coding: utf-8 -*-

from mixer.backend.flask import mixer

from .base import BasePayload


class NewsPayload(BasePayload):
    def __init__(self):
        super(NewsPayload, self).__init__('news')

    def set_title(self, title):
        self._set_attribute('title', title)
        return self

    def set_content(self, content):
        self._set_attribute('content', content)
        return self

    def set_username(self, username):
        self._set_attribute('username', username)
        return self

    def set_author(self, user_id):
        self._set_relationships('author', 'user', user_id)
        return self

    def set_obj(self, obj):
        self.set_title(obj.title)
        self.set_content(obj.content)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend('app.models.news.News'))
            return self
