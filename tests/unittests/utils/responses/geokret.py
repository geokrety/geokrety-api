# -*- coding: utf-8 -*-

from base import BaseResponse


class GeokretResponse(BaseResponse):

    @property
    def holder(self):
        self._get_attribute('holder')

    def assertHasRelationshipOwner(self, response, user):
        self.assertHasRelationship(response, 'owner', '/v1/users/%s' % (user.id))

    def assertHasRelationshipGeokretyType(self, response, geokrety_type):
        self.assertHasRelationship(response, 'type', '/v1/geokrety-types/%s' % (geokrety_type))

    def assertHasRelationshipMoves(self, response):
        self.assertHasRelationship(response, 'moves', '/v1/geokrety/%s/moves' % (response.id))

    def assertHasIncludeHolder(self, response, user):
        self.assertHasIncludeId(response, 'holder', user.id)

    def assertHasPublicAttributes(self, response, obj):
        self.assertHasAttribute(response, 'name', obj.name)
