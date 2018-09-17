# -*- coding: utf-8 -*-

from base import BaseResponse


class MoveResponse(BaseResponse):

    def assertHasRelationshipAuthor(self):
        self.assertHasRelationshipSelf('author', '/v1/moves/%s/relationships/author' % self.id)
        self.assertHasRelationshipRelated('author', '/v1/moves/%s/author' % self.id)

    def assertHasRelationshipMoveType(self):
        self.assertHasRelationshipSelf('type', '/v1/moves/%s/relationships/type' % self.id)
        self.assertHasRelationshipRelated('type', '/v1/moves/%s/type' % self.id)

    def assertHasRelationshipGeokret(self):
        self.assertHasRelationshipSelf('geokret', '/v1/moves/%s/relationships/geokret' % self.id)
        self.assertHasRelationshipRelated('geokret', '/v1/moves/%s/geokret' % self.id)

    def assertHasRelationshipAuthorData(self, user_id):
        self.assertHasRelationshipData('author', user_id, 'user')

    def assertHasRelationshipMoveTypeData(self, type_id):
        self.assertHasRelationshipData('type', type_id, 'move-type')

    def assertHasRelationshipGeokretData(self, geokret_id):
        self.assertHasRelationshipData('geokret', geokret_id, 'geokret')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('comment', obj.comment)
        self.assertHasAttribute('username', obj.username)
        self.assertHasAttributeDateTime('moved_on_datetime', obj.moved_on_datetime)
        self.assertHasAttribute('application_name', obj.application_name)
        self.assertHasAttribute('application_version', obj.application_version)
        self.assertHasAttribute('altitude', obj.altitude)
        self.assertHasAttribute('country', obj.country)
        self.assertHasAttribute('distance', obj.distance)
        self.assertHasAttribute('pictures_count', obj.pictures_count)
        self.assertHasAttribute('comments_count', obj.comments_count)
        self.assertHasAttributeDateTime('created_on_datetime', obj.created_on_datetime)
        self.assertHasAttributeDateTime('updated_on_datetime', obj.updated_on_datetime)
        self.assertHasRelationshipAuthor()
        self.assertHasRelationshipMoveType()
        self.assertHasRelationshipGeokret()
        self.assertHasRelationshipAuthorData(obj.author.id)
        self.assertHasRelationshipMoveTypeData(obj.type)
        self.assertHasRelationshipGeokretData(obj.geokret.id)
        with self.assertRaises(AssertionError):
            self.get_attribute('tracking_code')
