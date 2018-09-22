# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class NewsResponse(BaseResponse):

    @property
    def title(self):
        return self.get_attribute('title')

    @property
    def content(self):
        return self.get_attribute('content')

    @property
    def username(self):
        return self.get_attribute('username')

    @property
    def comments_count(self):
        return self.get_attribute('comments-count')

    @property
    def last_comment_date_time(self):
        return self.get_attribute('last-comment-date-time')

    @property
    def author(self):
        return self['relationships']['author']['data']['id']

    def assertHasRelationshipAuthor(self):
        self.assertHasRelationshipSelf('author', '/v1/news/%s/relationships/author' % self.id)
        self.assertHasRelationshipRelated('author', '/v1/news/%s/author' % self.id)

    def assertHasRelationshipNewsComments(self):
        self.assertHasRelationshipSelf('news-comments', '/v1/news/%s/relationships/news-comments' % self.id)
        self.assertHasRelationshipRelated('news-comments', '/v1/news/%s/news-comments' % self.id)

    def assertHasRelationshipAuthorData(self, news_id):
        self.assertHasRelationshipData('author', news_id, 'user')

    def assertHasRelationshipNewsCommentsData(self, news_id):
        self.assertHasRelationshipData('news-comments', news_id, 'news-comment')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('title', obj.title)
        self.assertHasAttribute('content', obj.content)
        self.assertHasAttribute('username', obj.username)
        self.assertHasAttribute('comments-count', obj.comments_count)
        self.assertHasAttribute('last-comment-date-time', obj.last_comment_date_time)
        self.assertHasRelationshipAuthor()
        self.assertHasRelationshipNewsComments()
