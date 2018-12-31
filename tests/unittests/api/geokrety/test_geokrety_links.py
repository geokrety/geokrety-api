# -*- coding: utf-8 -*-

from app.api.helpers.data_layers import GEOKRET_TYPE_HUMAN
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.geokret import GeokretPayload


class TestGeokretyDetailsLinks(BaseTestCase):
    """Test GeoKrety details links"""

    @request_context
    def test_get_geokrety_details_via_users_geokrety_owned(self):
        geokret = self.blend_geokret(owner=self.user_1)
        response = GeokretPayload(_url_collection="/v1/users/{}/geokrety-owned".format(geokret.owner.id))\
            .get_collection()\
            .assertCount(1)
        response.data[0].assertHasPublicAttributes(geokret)

    @request_context
    def test_get_geokrety_details_via_users_geokrety_owned_unexistent(self):
        self.blend_geokret(owner=self.user_1)
        GeokretPayload(_url_collection="/v1/users/{}/geokrety-owned".format(666))\
            .get_collection(code=404)\
            .assertRaiseJsonApiError('owner_id')

    @request_context
    def test_get_geokrety_details_via_users_geokrety_held(self):
        geokret = self.blend_geokret(holder=self.user_1)
        response = GeokretPayload(_url_collection="/v1/users/{}/geokrety-held".format(geokret.holder.id))\
            .get_collection()\
            .assertCount(1)
        response.data[0].assertHasPublicAttributes(geokret)

    @request_context
    def test_get_geokrety_details_via_users_geokrety_held_unexistent(self):
        self.blend_geokret(holder=self.user_1)
        GeokretPayload(_url_collection="/v1/users/{}/geokrety-held".format(666))\
            .get_collection(code=404)\
            .assertRaiseJsonApiError('holder_id')

    @request_context
    def test_get_geokrety_details_via_geokrety_types(self):
        geokret = self.blend_geokret(type=GEOKRET_TYPE_HUMAN)
        response = GeokretPayload(_url_collection="/v1/geokrety-types/{}/geokrety".format(GEOKRET_TYPE_HUMAN))\
            .get_collection()\
            .assertCount(1)
        response.data[0].assertHasPublicAttributes(geokret)

    @request_context
    def test_get_geokrety_details_via_geokrety_types_unexistent(self):
        self.blend_geokret(holder=self.user_1)
        GeokretPayload(_url_collection="/v1/geokrety-types/{}/geokrety".format(666))\
            .get_collection(code=404)\
            .assertRaiseJsonApiError('geokrety_type_id')
