# -*- coding: utf-8 -*-

import urllib
from decimal import Decimal

from parameterized import parameterized

from app.api.helpers.db import safe_query
from app.models.user import User
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.user import UserPayload
from tests.unittests.utils.responses.user import UserResponse
from tests.unittests.utils.static_test_cases import (NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestUserCreate(BaseTestCase):
    """Test User create"""

    def send_post(self, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/users?%s" % (args_)
        return UserResponse(self._send_post(url, payload=payload, **kwargs).get_json())

    @request_context
    def test_user_create_can_be_posted_as_anonymous(self):
        payload = UserPayload()
        self.send_post(payload)

    @parameterized.expand([
        ['admin', 403],
        ['user_1', 403],
        ['user_2', 403],
    ])
    @request_context
    def test_user_create_can_be_posted_as(self, username, expected):
        user = getattr(self, username) if username else None
        payload = UserPayload()
        self.send_post(payload, user=user, code=expected)

    @parameterized.expand([
        ['name'],
        ['email'],
        ['password'],
    ])
    @request_context
    def test_user_create_mandatory_field(self, attribute):
        payload = UserPayload()
        del payload['data']['attributes'][attribute]
        response = self.send_post(payload, code=422)
        response.assertRaiseJsonApiError('/data/attributes/{}'.format(attribute))

    @request_context
    def test_user_create_unicity_field_username(self):
        payload = UserPayload()
        name = payload['data']['attributes']['name']
        response = self.send_post(payload)
        payload.blend()
        payload.set_name(name)
        response = self.send_post(payload, code=422)
        response.assertRaiseJsonApiError('/data/attributes/name')

    @request_context
    def test_user_create_unicity_field_email(self):
        payload = UserPayload()
        email = payload['data']['attributes']['email']
        response = self.send_post(payload)
        payload.blend()
        payload.set_email(email)
        response = self.send_post(payload, code=422)
        response.assertRaiseJsonApiError('/data/attributes/email')

    @parameterized.expand([
        ['language'],
        ['country'],
        ['latitude'],
        ['longitude'],
        ['daily-mails'],
        ['observation-radius'],
        ['statpic-id'],
        ['hour'],
    ])
    @request_context
    def test_user_create_optionnal_fields(self, attribute):
        payload = UserPayload()
        del payload['data']['attributes'][attribute]
        self.send_post(payload)

    @request_context
    def test_user_create_backend_generate_secid(self):
        payload = UserPayload()
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertNotEqual(unicode(payload['data']['attributes']['secid']), user.secid)

    @request_context
    def test_user_create_backend_generate_join_date_time(self):
        payload = UserPayload()
        del payload['data']['attributes']['join-datetime']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        user.join_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    @request_context
    def test_user_create_backend_generate_last_update_datetime(self):
        payload = UserPayload()
        del payload['data']['attributes']['last-update-datetime']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        user.last_update_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    @request_context
    def test_user_create_backend_generate_last_mail_datetime(self):
        payload = UserPayload()
        del payload['data']['attributes']['last-mail-datetime']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.last_mail_datetime)

    @request_context
    def test_user_create_backend_generate_last_login_datetime(self):
        payload = UserPayload()
        del payload['data']['attributes']['last-login-datetime']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.last_login_datetime)

    @request_context
    def test_user_create_valid_email(self):
        payload = UserPayload()
        payload.set_email("A@VALID.EMAIL")
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertEqual(user.email, "A@VALID.EMAIL")

    @request_context
    def test_user_create_invalid_email(self):
        payload = UserPayload()
        payload.set_email("NOT_A_VALID_EMAIL")
        response = self.send_post(payload, code=422)
        response.assertRaiseJsonApiError('/data/attributes/email')

    @request_context
    def test_user_create_password_is_encrypted(self):
        import phpass
        phpass.PasswordHash.hash_password = self.hash_password_original
        payload = UserPayload()
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertNotEqual(user.password, payload['data']['attributes']['password'])
        self.assertEqual(user.password[:7], "$2a$11$")

    @request_context
    def test_user_create_languages_defaults_to_english_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['language']
        response = self.send_post(payload)
        response.assertHasAttribute('language', 'en')

    @request_context
    def test_user_create_languages_defaults_to_english_if_empty(self):
        payload = UserPayload()
        payload.set_language('')
        response = self.send_post(payload)
        response.assertHasAttribute('language', 'en')

    @parameterized.expand([
        ['en', 201],
        ['fr', 201],
        ['francais', 422],
        ['tt', 422],
        ['t', 422],
    ])
    @request_context
    def test_user_create_languages_are_checked_against_static_list(self, language, expected):
        payload = UserPayload()
        payload.set_language(language)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/language')
        else:
            response.assertHasAttribute('language', language)

    @parameterized.expand([
        ['fr', 201],
        ['pl', 201],
        ['de', 201],
        ['uk', 201],
        ['ru', 201],
        ['ro', 201],
        ['zz', 422],
    ])
    @request_context
    def test_user_create_countries_are_checked_against_static_list(self, country, expected):
        payload = UserPayload()
        payload.set_country(country)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/country')
        else:
            response.assertHasAttribute('country', country)

    @request_context
    def test_user_create_countries_defaults_to_none_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['country']
        response = self.send_post(payload)
        response.assertHasAttribute('country', None)

    @request_context
    def test_user_create_countries_defaults_to_none_if_empty(self):
        payload = UserPayload()
        payload.set_country('')
        response = self.send_post(payload)
        response.assertHasAttribute('country', None)

    @parameterized.expand([
        ['', 422],
        ['abc.def', 422],
        [u'0', 201],
        ['0', 201],
        ['0.0', 201],
        ['1', 201],
        ['1.0', 201],
        [0, 201],
        [0.0, 201],
        [1, 201],
        [1.0, 201],
    ])
    @request_context
    def test_user_create_home_latitude_as_decimal_degrees(self, latitude, expected):
        payload = UserPayload()
        payload.set_latitude(latitude)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/latitude')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.latitude, Decimal(latitude))

    @parameterized.expand([
        ['', 422],
        [' ', 422],
        ['abc.def', 422],
        [u'0', 201],
        ['0', 201],
        ['0.0', 201],
        ['1', 201],
        ['1.0', 201],
        [0, 201],
        [0.0, 201],
        [1, 201],
        [1.0, 201],
    ])
    @request_context
    def test_user_create_home_longitude_as_decimal_degrees(self, longitude, expected):
        payload = UserPayload()
        payload.set_longitude(longitude)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/longitude')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.longitude, Decimal(longitude))

    @request_context
    def test_user_create_home_latitude_default_to_null_if_empty(self):
        payload = UserPayload()
        payload.set_latitude(None)
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.latitude)

    @request_context
    def test_user_create_home_latitude_default_to_null_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['latitude']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.latitude)

    @request_context
    def test_user_create_home_longitude_default_to_null_if_empty(self):
        payload = UserPayload()
        payload.set_longitude(None)
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.longitude)

    @request_context
    def test_user_create_home_longitude_default_to_null_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['longitude']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertIsNone(user.longitude)

    @parameterized.expand([
        [None, 201],
        ['', 422],
        [' ', 422],
        ['a', 422],
        ['0', 201],
        ['0.0', 422],
        [0, 201],
        [0.0, 201],
        [1, 201, True],
        [1.0, 201, True],
        [1.1, 422],
    ])
    @request_context
    def test_user_create_field_daily_mails_is_boolean(self, value, expected_code, expected=False):
        payload = UserPayload()
        payload.set_daily_mails(value)
        response = self.send_post(payload, code=expected_code)
        if expected_code == 422:
            response.assertRaiseJsonApiError('/data/attributes/daily-mails')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.daily_mails, expected)

    @request_context
    def test_user_create_field_daily_mails_default_to_false_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['daily-mails']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertFalse(user.daily_mails)

    @parameterized.expand([
        ['', 422],
        [' ', 422],
        ['a', 422],
        ['0', 201],
        ['0.0', 422],
        [0, 201],
        [0.0, 201],
        [1, 201],
        [1.0, 201],
        [1.1, 201],
    ])
    @request_context
    def test_user_create_field_observation_radius_is_integer(self, radius, expected):
        payload = UserPayload()
        payload.set_observation_radius(radius)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/observation-radius')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.observation_radius, int(radius))

    @request_context
    def test_user_create_field_observation_radius_default_to_zero_if_empty(self):
        payload = UserPayload()
        payload.set_observation_radius(None)
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertEqual(user.observation_radius, 0)

    @request_context
    def test_user_create_field_observation_radius_default_to_zero_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['observation-radius']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertEqual(user.observation_radius, 0)

    @parameterized.expand([
        [-1, 422],
        [0, 201],
        [1, 201],
        [2, 201],
        [8, 201],
        [9, 201],
        [10, 201],
        [11, 422],
        [666, 422],
    ])
    @request_context
    def test_user_create_field_observation_radius_is_betwwen_zero_ten(self, radius, expected):
        payload = UserPayload()
        payload.set_observation_radius(radius)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/observation-radius')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.observation_radius, int(radius))

    @parameterized.expand([
        ['', 422],
        [' ', 422],
        ['a', 422],
        ['0', 201],
        ['0.0', 422],
        [0, 201],
        [0.0, 201],
        [1, 201],
        [1.0, 201],
        [1.1, 201],
    ])
    @request_context
    def test_user_create_field_hour_is_integer(self, hour, expected):
        payload = UserPayload()
        payload.set_hour(hour)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/hour')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.hour, int(hour))

    @parameterized.expand([
        [-1, 422],
        [0, 201],
        [1, 201],
        [2, 201],
        [8, 201],
        [9, 201],
        [10, 201],
        [11, 201],
        [21, 201],
        [22, 201],
        [23, 201],
        [24, 422],
        [666, 422],
    ])
    @request_context
    def test_user_create_field_hour_is_betwwen_zero_ten(self, hour, expected):
        payload = UserPayload()
        payload.set_hour(hour)
        response = self.send_post(payload, code=expected)
        if expected == 422:
            response.assertRaiseJsonApiError('/data/attributes/hour')
        else:
            user = safe_query(self, User, 'id', response.id, 'id')
            self.assertEqual(user.hour, int(hour))

    @request_context
    def test_user_create_field_hour_default_to_zero_if_random(self):
        payload = UserPayload()
        payload.set_hour(None)
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertGreaterEqual(user.hour, 0)
        self.assertLessEqual(user.hour, 23)

    @request_context
    def test_user_create_field_hour_default_to_zero_if_missing(self):
        payload = UserPayload()
        del payload['data']['attributes']['observation-radius']
        response = self.send_post(payload)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertGreaterEqual(user.hour, 0)
        self.assertLessEqual(user.hour, 23)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_user_create_field_username_support_utf8(self, username, expected):
        payload = UserPayload()
        payload.set_name(username)
        response = self.send_post(payload)
        response.assertHasAttribute('name', expected)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertEqual(user.name, expected)

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_user_create_field_username_cannot_be_blank(self, username, expected):
        payload = UserPayload()
        payload.set_name(username)
        response = self.send_post(payload)
        response.assertHasAttribute('name', expected)
        user = safe_query(self, User, 'id', response.id, 'id')
        self.assertEqual(user.name, expected)
