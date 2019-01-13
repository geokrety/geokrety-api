# -*- coding: utf-8 -*-

from app.models.user import User

from .base import BaseResponse
from .collections import BaseCollectionResponse


class BadgeResponse(BaseResponse):

    def assertHasRelationshipAuthor(self):
        self.assertHasRelationshipSelf('author', '/v1/badges/%s/relationships/author' % self.id)
        self.assertHasRelationshipRelated('author', '/v1/badges/%s/author' % self.id)
        return self

    def assertHasRelationshipAuthorData(self, user):
        user_id = user.id if isinstance(user, User) else user
        self.assertHasRelationshipData('author', user_id, 'user')
        return self

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('description', obj.description)
        self.assertHasAttribute('filename', obj.filename)
        self.assertHasAttributeDateTime('created_on_datetime', obj.created_on_datetime)
        self.assertHasRelationshipAuthor()
        return self


class BadgeCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(BadgeCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(BadgeResponse(data_))
        self['data'] = datas
