# -*- coding: utf-8 -*-

from app.api.helpers.data_layers import GEOKRET_TYPE_HUMAN
from tests.unittests.utils.base_test_case import BaseTestCase, request_context


class TestGeokretyRelationships(BaseTestCase):
    """Test GeoKrety relationships"""

    def validate(self, url, item_id):
        response = self._send_get(url.format(self.geokret.id), user=self.user_2).get_json()
        self.assertEqual(response['data']['id'], item_id)

    @request_context
    def test_geokrety_owner_relationship(self):
        self.geokret = self.blend_geokret(owner=self.user_1)
        url = "/v1/geokrety/{}/relationships/owner"
        self.validate(url, self.user_1.id)

    @request_context
    def test_geokrety_holder_relationship(self):
        self.geokret = self.blend_geokret(holder=self.user_1)
        url = "/v1/geokrety/{}/relationships/holder"
        self.validate(url, self.user_1.id)

    @request_context
    def test_geokrety_type_relationship(self):
        self.geokret = self.blend_geokret(type=GEOKRET_TYPE_HUMAN)
        url = "/v1/geokrety/{}/relationships/type"
        self.validate(url, GEOKRET_TYPE_HUMAN)
