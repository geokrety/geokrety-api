# -*- coding: utf-8 -*-

from base import BaseResponse


class GeokretyTypesResponse(BaseResponse):

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        # self.assertHasRelationshipGeokrety()  # # Seems not supported by framework
