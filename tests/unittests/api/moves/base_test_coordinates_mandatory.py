# -*- coding: utf-8 -*-

from parameterized import parameterized

from base_test_coordinates import _BaseTestCoordinates
from tests.unittests.utils.base_test_case import request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.static_test_cases import FLOAT_TESTS_CASES


class _BaseTestCoordinatesMandatory(_BaseTestCoordinates):
    """Base tests with mandatory coordinates"""

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        assert self.send_post(payload, user=user)

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_field_latitude_must_be_present(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('latitude', None)
        response = self.send_post(payload, user=user, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_field_longitude_must_be_present(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('longitude', None)
        response = self.send_post(payload, user=user, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [None],
        [u''],
    ])
    @request_context
    def test_field_latitude_cannot_be_empty(self, latitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('latitude', latitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand([
        [None],
        [u''],
    ])
    @request_context
    def test_field_longitude_cannot_be_empty(self, longitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('longitude', longitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')
