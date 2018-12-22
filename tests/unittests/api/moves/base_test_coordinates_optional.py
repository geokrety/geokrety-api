# -*- coding: utf-8 -*-

from parameterized import parameterized

from base_test_move_create import _BaseTestMoveCreate
from tests.unittests.utils.base_test_case import request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.static_test_cases import (BLANK_CHARACTERS_TEST_CASES,
                                                     EMPTY_TEST_CASES,
                                                     FLOAT_TESTS_CASES)


class _BaseTestCoordinatesOptional(_BaseTestMoveCreate):
    """Base tests with optional coordinates"""

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_move_create_optional_coordinates_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        assert self.send_post(payload, user=user)

    @request_context
    def test_move_create_optional_coordinates_field_tracking_code_must_be_present(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        del payload['data']['attributes']['tracking-code']
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_move_create_optional_coordinates_field_tracking_code_cannot_be_blank(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @request_context
    def test_move_create_optional_coordinates_field_altitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('altitude', -32768)

    @request_context
    def test_move_create_optional_coordinates_field_country_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('country', '')

    @request_context
    def test_move_create_optional_coordinates_field_distance_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('distance', 0)

    @request_context
    def test_move_create_optional_coordinates_field_waypoint_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @request_context
    def test_move_create_optional_coordinates_field_latitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)

    @request_context
    def test_move_create_optional_coordinates_field_longitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('longitude', None)

    @parameterized.expand([
        [None],
        [u''],
    ])
    @request_context
    def test_move_create_optional_coordinates_field_waypoint_can_be_empty(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @parameterized.expand([
        [u'ééééé'],
        [u'<'],
        [u'\x01 '],
        [u'";!'],
    ])
    @request_context
    def test_move_create_optional_coordinates_field_tracking_code_must_be_alphanumeric(self, tracking_code):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_tracking_code(tracking_code)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

    @parameterized.expand([
        [u'ééééé'],
        [u'<'],
        [u'\x01 '],
        [u'";!'],
    ])
    @request_context
    def test_move_create_optional_coordinates_field_waypoint_must_be_alphanumeric(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/waypoint')

    @parameterized.expand(BLANK_CHARACTERS_TEST_CASES)
    @request_context
    def test_move_create_optional_coordinates_field_waypoint_dont_accept_blank_characters(self, waypoint):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_waypoint(waypoint)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/waypoint')

    @parameterized.expand(FLOAT_TESTS_CASES)
    @request_context
    def test_move_create_optional_coordinates_field_latitude_must_be_decimal(self, latitude, expected):
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
    def test_move_create_optional_coordinates_field_longitude_must_be_decimal(self, longitude, expected):
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
    def test_move_create_optional_coordinates_field_latitude_must_be_valid(self, latitude):
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
    def test_move_create_optional_coordinates_field_longitude_must_be_valid(self, longitude):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates()
        payload.set_coordinates(0.0, longitude)
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @parameterized.expand([
        [0.0, None, 422, 'longitude'],
        [None, 0.0, 422, 'latitude'],
    ])
    @request_context
    def test_move_create_optional_coordinates_field_when_one_coordinate_parameter_is_given_the_other_must_be_provided(self, latitude, longitude, expected, field=None):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates(latitude, longitude)
        response = self.send_post(payload, user=self.user_1, code=expected)
        response.assertRaiseJsonApiError('/data/attributes/{}'.format(field))

    @request_context
    def test_move_create_optional_coordinates_field_latitude_longitude_may_be_both_none(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates(None, None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)
        response.assertHasAttribute('longitude', None)
