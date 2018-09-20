# -*- coding: utf-8 -*-

import json
import pprint
import unittest
from datetime import date, datetime

import phpass
from mixer.backend.flask import mixer
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         GEOKRET_TYPES_TEXT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPES_TEXT)
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.user import User
from tests.unittests.setup_database import Setup


def mock_hash_password(obj, password):
    """Mock hash_password from phpass.PasswordHash"""
    return password


def mock_check_password(obj, password_1, password_2):
    """Mock check_password from phpass.PasswordHash"""
    return password_1 == password_2


# https://stackoverflow.com/a/22238613/944936
def json_serial(obj):  # pragma: no cover
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type %s not serializable" % type(obj))


def custom_name_geokrety_type(testcase_func, param_num, param):
    id = unicode(param.args[0])
    name = GEOKRET_TYPES_TEXT[id] if id in GEOKRET_TYPES_TEXT else id
    return u"%s_%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name),
        testcase_func.__name__,
    )


def custom_name_geokrety_move_type(testcase_func, param_num, param):
    id = unicode(param.args[0])
    name = MOVE_TYPES_TEXT[id] if id in MOVE_TYPES_TEXT else id
    return u"%s_%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name),
        testcase_func.__name__,
    )


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Setup.drop_db()
        self.app = Setup.create_app()
        phpass.PasswordHash.hash_password = mock_hash_password
        phpass.PasswordHash.check_password = mock_check_password
        mixer.init_app(app)

    @classmethod
    def tearDownClass(self):
        Setup.drop_db()

    def tearDown(self):
        Setup.truncate_db()

    def blend_admin(self, *args, **kwargs):
        with mixer.ctx():
            return mixer.blend(User, is_admin=True, **kwargs)

    def blend_user(self, *args, **kwargs):
        with mixer.ctx():
            return mixer.blend(User, **kwargs)

    def blend_move(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(Move, **kwargs)
            return mixer.blend(Move, **kwargs)

    def blend_users(self, count=3, *args, **kwargs):
        self.admin = self.blend_admin(**kwargs)
        for i in range(1, count):
            setattr(self, 'user_{}'.format(i), self.blend_user(**kwargs))

    def blend_geokret(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(Geokret, **kwargs)
            return mixer.blend(Geokret, **kwargs)

    def _login(self, username="kumy", password="password"):
        """
        Obtain a JWT token to authenticate next requests
        """
        response = self.app.post('/auth/session',
                                 headers={
                                     'content-type': 'application/json'
                                 },
                                 data=json.dumps({
                                     "username": username,
                                     "password": password
                                 }), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Content-Type' in response.headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        raised = False
        try:
            data = json.loads(response.data)
        except Exception:  # pragma: no cover
            raised = True
        self.assertFalse(raised, 'Failed to decode json')
        self.assertTrue('access_token' in data)
        return data['access_token']

    def _send(self,
              method,
              endpoint,
              code=200,
              payload=None,
              user=None,
              content_type='application/vnd.api+json; charset=utf8'):
        """
        Send a POST request to the api, and check expected response code.
        """
        if not payload:
            payload = {}

        headers = {}
        if user:
            headers['Authorization'] = \
                'JWT %s' % self._login(user.name, user.password)

        with app.test_request_context():
            response = getattr(self.app, method)(endpoint,
                                               json=payload,
                                               headers=headers,
                                               content_type=content_type)

            data = response.get_data(as_text=False)
            if response.content_type in ['application/vnd.api+json', 'application/json'] and data:
                data = json.loads(data)

            if response.status_code != code:  # pragma: no cover
                pprint.pprint(data)

            self.assertEqual(response.status_code, code)
            return response

    def _send_post(self,
                   endpoint,
                   code=201,
                   payload=None,
                   user=None,
                   content_type='application/vnd.api+json'):
        return self._send('post',
                          endpoint,
                          code=code,
                          payload=payload,
                          user=user,
                          content_type=content_type)

    def _send_get(self,
                  endpoint,
                  code=200,
                  payload=None,
                  user=None,
                  content_type='application/vnd.api+json'):
        return self._send('get',
                          endpoint,
                          code=code,
                          payload=payload,
                          user=user,
                          content_type=content_type)

    def _send_patch(self,
                    endpoint,
                    code=200,
                    payload=None,
                    user=None,
                    content_type='application/vnd.api+json'):
        return self._send('patch',
                          endpoint,
                          code=code,
                          payload=payload,
                          user=user,
                          content_type=content_type)

    def _send_delete(self,
                     endpoint,
                     code=200,
                     payload=None,
                     user=None,
                     content_type='application/vnd.api+json'):
        return self._send('delete',
                          endpoint,
                          code=code,
                          payload=payload,
                          user=user,
                          content_type=content_type)

    # def assertDateTimeEqual(self, datetime_str, datetime_obj):
    #     if isinstance(datetime_obj, str):   # pragma: no cover
    #         # Check date is parsable
    #         raised = False
    #         try:
    #             datetime.strptime(datetime_obj, "%Y-%m-%dT%H:%M:%S")
    #         except Exception:
    #             raised = True
    #         self.assertFalse(raised, 'Date is not parsable')
    #     else:
    #         self.assertEqual(datetime_str, datetime_obj.strftime("%Y-%m-%dT%H:%M:%S"))

    # def assertDateEqual(self, date_str, date_obj):
    #     if isinstance(date_obj, str):
    #         # Check date is parsable
    #         raised = False
    #         try:
    #             datetime.strptime(date_obj, "%Y-%m-%d")
    #         except Exception:  # pragma: no cover
    #             raised = True
    #         self.assertFalse(raised, 'Date is not parsable')
    #     else:
    #         self.assertEqual(date_str, date_obj.strftime("%Y-%m-%d"))

    # def _check_geokret(self, data, geokret, skip_check=None, with_private=False):
    #     skip_check = skip_check or []
    #     self.assertTrue('attributes' in data)
    #     attributes = data['attributes']
    #
    #     self.assertTrue('name' in attributes)
    #     self.assertTrue('description' in attributes)
    #     self.assertTrue('missing' in attributes)
    #     self.assertTrue('distance' in attributes)
    #     self.assertTrue('caches-count' in attributes)
    #     self.assertTrue('pictures-count' in attributes)
    #     self.assertTrue('average-rating' in attributes)
    #     self.assertTrue('created-on-datetime' in attributes)
    #     self.assertTrue('updated-on-datetime' in attributes)
    #
    #     self.assertEqual(attributes['name'], geokret.name)
    #     self.assertEqual(attributes['description'], geokret.description)
    #     self.assertEqual(attributes['missing'], geokret.missing)
    #     self.assertEqual(attributes['distance'], geokret.distance)
    #     self.assertEqual(attributes['caches-count'], geokret.caches_count)
    #     self.assertEqual(attributes['pictures-count'], geokret.pictures_count)
    #     self.assertEqual(attributes['average-rating'], geokret.average_rating)
    #
    #     if 'times' not in skip_check:
    #         self.assertDateTimeEqual(attributes['created-on-datetime'], geokret.created_on_datetime)
    #         self.assertDateTimeEqual(attributes['updated-on-datetime'], geokret.updated_on_datetime)
    #
    #     if with_private is not None:
    #         self.assertTrue('attributes' in data)
    #         attributes = data['attributes']
    #
    #         self.assertTrue('tracking-code' in attributes)
    #         if with_private:
    #             if 'tracking-code' not in skip_check:
    #                 self.assertEqual(attributes['tracking-code'], geokret.tracking_code)
    #         else:
    #             self.assertIsNone(attributes['tracking-code'])
    #
    # def _check_move(self, data, move, skip_check=None):
    #     skip_check = skip_check or []
    #     self.assertTrue('attributes' in data)
    #     attributes = data['attributes']
    #
    #     self.assertTrue('move-type-id' in attributes)
    #     self.assertTrue('altitude' in attributes)
    #     self.assertTrue('country' in attributes)
    #     self.assertTrue('distance' in attributes)
    #     self.assertTrue('comment' in attributes)
    #     self.assertTrue('username' in attributes)
    #     self.assertTrue('application-name' in attributes)
    #     self.assertTrue('application-version' in attributes)
    #     self.assertTrue('pictures-count' in attributes)
    #     self.assertTrue('comments-count' in attributes)
    #     self.assertTrue('moved-on-datetime' in attributes)
    #     self.assertTrue('created-on-datetime' in attributes)
    #     self.assertTrue('updated-on-datetime' in attributes)
    #
    #     self.assertEqual(attributes['move-type-id'], move.move_type_id)
    #     self.assertEqual(attributes['altitude'], move.altitude)
    #     self.assertEqual(attributes['country'], move.country)
    #     self.assertEqual(attributes['distance'], move.distance)
    #     self.assertEqual(attributes['comment'], move.comment)
    #     self.assertEqual(attributes['username'], move.username)
    #     self.assertEqual(attributes['application-name'], move.application_name)
    #     self.assertEqual(attributes['application-version'], move.application_version)
    #     self.assertEqual(attributes['pictures-count'], move.pictures_count)
    #     self.assertEqual(attributes['comments-count'], move.comments_count)
    #
    #     if attributes['moved-on-datetime'] is not None:
    #         self.assertDateTimeEqual(attributes['moved-on-datetime'], move.moved_on_datetime)
    #
    #     if attributes['move-type-id'] in (MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN, MOVE_TYPE_DIPPED):
    #         self.assertTrue('latitude' in attributes)
    #         self.assertTrue('longitude' in attributes)
    #         self.assertTrue('waypoint' in attributes)
    #         self.assertEqual(attributes['latitude'], float(move.latitude))
    #         self.assertEqual(attributes['longitude'], float(move.longitude))
    #         self.assertEqual(attributes['waypoint'], move.waypoint)
    #
    #     if 'times' not in skip_check:
    #         self.assertDateTimeEqual(attributes['created-on-datetime'], move.created_on_datetime)
    #         self.assertDateTimeEqual(attributes['updated-on-datetime'], move.updated_on_datetime)
