# -*- coding: utf-8 -*-

from datetime import datetime

from base import BaseResponse


class MovesTypesResponse(BaseResponse):

    @property
    def name(self):
        return self.get_attribute('name')

    def assertHasRelationshipMoves(self):
        self.assertHasRelationshipSelf('moves', '/v1/geokrety-types/%s/relationships/moves' % self.id)
        self.assertHasRelationshipRelated('moves', '/v1/geokrety-types/%s/moves' % self.id)

    def assertHasRelationshipMovesData(self, move_type_id):
        self.assertHasRelationshipData('moves', move_type_id, 'move')

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        # self.assertHasRelationshipMoves()  # # Seems not supported by framework
