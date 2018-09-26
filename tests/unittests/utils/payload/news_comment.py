# -*- coding: utf-8 -*-

from mixer.backend.flask import mixer

from .base import BasePayload


class NewsCommentPayload(BasePayload):
    def __init__(self):
        super(NewsCommentPayload, self).__init__('news-comment')

    def set_comment(self, comment):
        self._set_attribute('comment', comment)
        return self

    def set_icon(self, icon):
        self._set_attribute('icon', icon)
        return self

    def set_author(self, user_id):
        self._set_relationships('author', 'user', user_id)
        return self

    def set_news(self, news_id):
        self._set_relationships('news', 'news', news_id)
        return self

    def set_obj(self, obj):
        self._set_attribute('created_on_datetime', obj.created_on_datetime)
        self.set_comment(obj.comment)
        self.set_icon(obj.icon)
        if obj.author.id:
            self.set_user(obj.author.id)
        if obj.news.id:
            self.set_news(obj.news.id)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend('app.models.news_comment.NewsComment'))
            return self
