# -*- coding: utf-8 -*-

from app.api.helpers.data_layers import GEOKRET_TYPE_HUMAN
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.responses.collections import \
    GeokretCollectionResponse


class TestGeokretyDetailsLinks(BaseTestCase):
    """Test GeoKrety details links"""

    def validate(self, url, pointer=None, **kwargs):
        response = GeokretCollectionResponse(self._send_get(url, user=self.user_2, **kwargs).get_json())
        if kwargs.get('code') == 404:
            response.assertRaiseJsonApiError(pointer)
        else:
            response.data[0].assertHasPublicAttributes(self.geokret)

    @request_context
    def test_geokrety_details_via_users_geokrety_owned(self):
        self.geokret = self.blend_geokret(owner=self.user_1)
        url = "/v1/users/{}/geokrety-owned".format(self.user_1.id)
        self.validate(url)

    @request_context
    def test_geokrety_details_via_users_geokrety_owned_unexistent(self):
        url = "/v1/users/{}/geokrety-owned".format(666)
        self.validate(url, code=404, pointer='owner_id')

    @request_context
    def test_geokrety_details_via_users_geokrety_held(self):
        self.geokret = self.blend_geokret(holder=self.user_1)
        url = "/v1/users/{}/geokrety-held".format(self.user_1.id)
        self.validate(url)

    @request_context
    def test_geokrety_details_via_users_geokrety_held_unexistent(self):
        url = "/v1/users/{}/geokrety-held".format(666)
        self.validate(url, code=404, pointer='holder_id')

    @request_context
    def test_geokrety_details_via_geokrety_types(self):
        self.geokret = self.blend_geokret(type=GEOKRET_TYPE_HUMAN)
        url = "/v1/geokrety-types/{}/geokrety".format(GEOKRET_TYPE_HUMAN)
        self.validate(url)

    @request_context
    def test_geokrety_details_via_geokrety_types_unexistent(self):
        url = "/v1/geokrety-types/{}/geokrety".format(666)
        self.validate(url, code=404, pointer='geokrety_type_id')
