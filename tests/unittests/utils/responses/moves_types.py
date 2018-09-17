# -*- coding: utf-8 -*-

from base import BaseResponse


class MovesTypesResponse(BaseResponse):

    def assertHasPublicAttributes(self, obj):
        self.assertHasAttribute('name', obj.name)
        # self.assertHasRelationshipMoves()  # # Seems not supported by framework
