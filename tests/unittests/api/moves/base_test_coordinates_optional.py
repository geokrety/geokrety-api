# -*- coding: utf-8 -*-

from parameterized import parameterized

from base_test_coordinates import _BaseTestCoordinates
from tests.unittests.utils.base_test_case import request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.static_test_cases import (BLANK_CHARACTERS_TEST_CASES,
                                                     EMPTY_TEST_CASES,
                                                     FLOAT_TESTS_CASES)


class _BaseTestCoordinatesOptional(_BaseTestCoordinates):
    """Base tests with optional coordinates"""

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
        ['admin'],
    ])
    @request_context
    def test_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        assert self.send_post(payload, user=user)

    @request_context
    def test_field_altitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('altitude', -32768)

    @request_context
    def test_field_country_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('country', '')

    @request_context
    def test_field_distance_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('distance', 0)

    @request_context
    def test_field_waypoint_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('waypoint', '')

    @request_context
    def test_field_latitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)

    @request_context
    def test_field_longitude_default_value(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('longitude', None)

    @parameterized.expand([
        [0.0, None, 422, 'longitude'],
        [None, 0.0, 422, 'latitude'],
    ])
    @request_context
    def test_field_latitude_longitude_must_be_provided_at_the_same_time(self, latitude, longitude, expected, field=None):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates(latitude, longitude)
        response = self.send_post(payload, user=self.user_1, code=expected)
        response.assertRaiseJsonApiError('/data/attributes/{}'.format(field))

    @request_context
    def test_field_latitude_longitude_may_be_both_none(self):
        geokret = self.blend_geokret()
        payload = MovePayload(self.move_type, geokret=geokret)\
            .set_coordinates(None, None)
        response = self.send_post(payload, user=self.user_1, code=201)
        response.assertHasAttribute('latitude', None)
        response.assertHasAttribute('longitude', None)