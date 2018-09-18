# -*- coding: utf-8 -*-

from base import BaseResponse


class GeokretResponse(BaseResponse):

    @property
    def holder(self):
        self._get_attribute('holder')

    def assertHasRelationshipOwner(self, user, response):
        self.assertHasRelationship('owner', '/v1/users/%s' % (user.id), response)

    def assertHasRelationshipGeokretyType(self, geokrety_type, response):
        self.assertHasRelationship('type', '/v1/geokrety-types/%s' % (geokrety_type), response)

    def assertHasRelationshipMoves(self, response):
        self.assertHasRelationship('moves', '/v1/geokrety/%s/moves' % (response.id), response)

    def assertHasIncludeHolder(self, response, user):
        self.assertHasIncludeId('holder', user.id, response)
