# -*- coding: utf-8 -*-

from base import BaseResponse


class NewsCommentResponse(BaseResponse):

    def assertHasComment(self, value):
        self.assertHasAttribute('comment', value)

    def assertHasRelationshipAuthor(self):
        self.assertHasRelationshipSelf('author', '/v1/news-comments/%s/relationships/author' % self.id)
        self.assertHasRelationshipRelated('author', '/v1/news-comments/%s/author' % self.id)

    def assertHasRelationshipNews(self):
        self.assertHasRelationshipSelf('news', '/v1/news-comments/%s/relationships/news' % self.id)
        self.assertHasRelationshipRelated('news', '/v1/news-comments/%s/news' % self.id)

    def assertHasRelationshipAuthorData(self, user_id):
        self.assertHasRelationshipData('author', user_id, 'user')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('comment', obj.comment)
        self.assertHasAttribute('icon', obj.icon)
        self.assertCreationDateTime()
        self.assertHasRelationshipAuthor()
        self.assertHasRelationshipAuthorData(obj.author.id)
        self.assertHasRelationshipNews()
