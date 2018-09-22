# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN,
                                         MOVE_TYPES_TEXT)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type)
from tests.unittests.utils.payload.geokret import GeokretyPayload
from tests.unittests.utils.responses.collections import GeokretResponse


class TestGeokretyEdit(BaseTestCase):
    """Test edit Geokrety"""

    def send_patch(self, id, payload=None, **kwargs):
        url = "/v1/geokrety/%s" % id
        return GeokretResponse(self._send_patch(url, payload=payload, **kwargs).get_json())

    #

    def test_patch_geokret_as_anonymous(self):
        with app.test_request_context():
            geokret = self.blend_geokret()
            self.send_patch(geokret.id, user=None, code=401)

    def test_patch_geokret_as_authenticated(self):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret()
            self.assertNotEqual(geokret.name, new_name)
            payload['data']['id'] = str(geokret.id)
            response = self.send_patch(geokret.id, payload=payload, user=self.user_1, code=403)

    def test_patch_geokret_as_admin(self):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret()
            self.assertNotEqual(geokret.name, new_name)
            payload['data']['id'] = str(geokret.id)
            response = self.send_patch(geokret.id, payload=payload, user=self.admin, code=200)
            self.assertEqual(response.name, new_name)

    def test_patch_geokret_as_owner(self):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_1)
            self.assertNotEqual(geokret.name, new_name)
            payload['data']['id'] = str(geokret.id)
            del payload['data']['relationships']

            response = self.send_patch(geokret.id, payload=payload, user=self.user_1, code=200)
            self.assertEqual(response.name, new_name)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_ARCHIVED],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    def test_patch_geokret_when_user_has_touched(self, input):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(created_on_datetime="2018-09-22T18:18:55")
            self.blend_move(geokret=geokret, author=self.user_1, move_type_id=input, moved_on_datetime="2018-09-22T18:18:56")
            self.blend_move(geokret=geokret, author=self.user_2, move_type_id=MOVE_TYPE_GRABBED,
                            moved_on_datetime="2018-09-22T18:18:57")
            response = self.send_patch(geokret.id, payload=payload, user=self.user_1, code=403)
