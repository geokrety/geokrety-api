# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class GeokretyTypesResponse(BaseResponse):

    @property
    def name(self):
        return self.get_attribute('subscribed')

    def assertHasRelationshipGeokrety(self):
        self.assertHasRelationshipSelf('geokrety', '/v1/geokrety-types/%s/relationships/geokret' % self.id)
        self.assertHasRelationshipRelated('geokrety', '/v1/geokrety-types/%s/geokret' % self.id)

    def assertHasRelationshipGeokretyData(self, geokrety_type_id):
        self.assertHasRelationshipData('geokrety', geokrety_type_id, 'geokret')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        # self.assertHasRelationshipGeokrety()  # # Seems not supported by framework
