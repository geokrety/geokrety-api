# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class NewsCommentResponse(BaseResponse):

    @property
    def comment(self):
        return self.get_attribute('comment')

    @property
    def icon(self):
        return self.get_attribute('icon')

    @property
    def user(self):
        return self['relationships']['user']['data']['id']

    @property
    def news(self):
        return self['relationships']['news']['data']['id']

    def assertHasComment(self, value):
        self.assertHasAttribute('comment', value)

    def assertHasIcon(self, value):
        self.assertHasAttribute('icon', value)

    def assertHasRelationshipAuthor(self):
        self.assertHasRelationshipSelf('author', '/v1/news-comments/%s/relationships/author' % self.id)
        self.assertHasRelationshipRelated('author', '/v1/news-comments/%s/author' % self.id)

    def assertHasRelationshipNews(self):
        self.assertHasRelationshipSelf('news', '/v1/news-comments/%s/relationships/news' % self.id)
        self.assertHasRelationshipRelated('news', '/v1/news-comments/%s/news' % self.id)

    def assertHasRelationshipAuthorData(self, user_id):
        self.assertHasRelationshipData('author', user_id, 'user')

    def assertHasRelationshipNewsData(self, news_id):
        self.assertHasRelationshipData('news', news_id, 'news')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('comment', obj.comment)
        self.assertHasAttribute('icon', obj.icon)
        self.assertCreationDateTime()
        self.assertHasRelationshipAuthor()
        self.assertHasRelationshipAuthorData(obj.author.id)
        self.assertHasRelationshipNews()
