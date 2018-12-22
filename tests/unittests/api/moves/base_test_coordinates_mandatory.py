# -*- coding: utf-8 -*-

from parameterized import parameterized

from base_test_move_create import _BaseTestMoveCreate
from tests.unittests.utils.base_test_case import request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.static_test_cases import FLOAT_TESTS_CASES


class _BaseTestCoordinatesMandatory(_BaseTestMoveCreate):
    """Base tests with mandatory coordinates"""

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_move_create_mandatory_coordinates_as(self, username):
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
    def test_move_create_mandatory_coordinates_field_waypoint_can_be_absent(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload['data']['attributes'].pop('waypoint', None)
        response = self.send_post(payload, user=user, code=201)
        response.assertHasAttribute('waypoint', '')

    @parameterized.expand([
        [None],
        [u''],
    ])
    @request_context
    def test_move_create_mandatory_coordinates_field_waypoint_can_be_empty(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_move_create_mandatory_coordinates_field_latitude_must_be_present(self, username):
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
    def test_move_create_mandatory_coordinates_field_longitude_must_be_present(self, username):
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
    def test_move_create_mandatory_coordinates_field_latitude_cannot_be_empty(self, latitude):
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
    def test_move_create_mandatory_coordinates_field_longitude_cannot_be_empty(self, longitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload._set_attribute('longitude', longitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand(FLOAT_TESTS_CASES)
    @request_context
    def test_move_create_mandatory_coordinates_field_latitude_must_be_decimal(self, latitude, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(latitude, 0.0)
        if expected == 201:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertHasAttribute('latitude', latitude)
        else:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand(FLOAT_TESTS_CASES)
    @request_context
    def test_move_create_mandatory_coordinates_field_longitude_must_be_decimal(self, longitude, expected):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(0.0, longitude)
        if expected == 201:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertHasAttribute('longitude', longitude)
        else:
            response = self.send_post(payload, user=self.user_1, code=expected)
            response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [-180.0],
        [-91.0],
        [-90.1],
        [-90.001],
        [90.001],
        [90.1],
        [91.0],
        [180.0],
    ])
    @request_context
    def test_move_create_mandatory_coordinates_field_latitude_must_be_valid(self, latitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(latitude, 0.0)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')

    @parameterized.expand([
        [-250.0],
        [-181.0],
        [-180.1],
        [-180.001],
        [180.001],
        [180.1],
        [181.0],
        [250.0],
    ])
    @request_context
    def test_move_create_mandatory_coordinates_longitude_must_be_valid(self, longitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(0.0, longitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')
