# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class GeokretResponse(BaseResponse):

    @property
    def holder(self):
        return self._get_attribute('holder')

    @property
    def created_on_datetime(self):
        import pprint
        pprint.pprint(self)
        return datetime.strptime(self._get_attribute('created-on-datetime'), '%Y-%m-%dT%H:%M:%S')

    @property
    def updated_on_datetime(self):
        return datetime.strptime(self._get_attribute('updated-on-datetime'), '%Y-%m-%dT%H:%M:%S')

    def assertHasRelationshipOwner(self, user):
        self.assertHasRelationship('owner', '/v1/users/%s' % (user.id))

    def assertHasRelationshipGeokretyType(self, geokrety_type):
        self.assertHasRelationship('type', '/v1/geokrety-types/%s' % (geokrety_type))

    def assertHasRelationshipMoves(self):
        self.assertHasRelationship('moves', '/v1/geokrety/%s/moves' % (self.id))

    def assertHasIncludeHolder(self, user):
        self.assertHasIncludeId('holder', user.id)

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('description', obj.description)
        self.assertHasAttribute('name', obj.name)
        self.assertHasAttribute('name', obj.name)
        self.pprint()
