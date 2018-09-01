import json
import pprint
import random
import unittest
from datetime import date, datetime, timedelta

import phpass
import responses
from app import current_app as app
from app.api.helpers.data_layers import (MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_SEEN)
from app.models.move import Move
from mixer.backend.flask import mixer
from tests.unittests.setup_database import Setup


# https://stackoverflow.com/a/22238613/944936
def json_serial(obj):  # pragma: no cover
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type %s not serializable" % type(obj))


def mock_hash_password(obj, password):
    """Mock hash_password from phpass.PasswordHash"""
    return password


def mock_check_password(obj, password_1, password_2):
    """Mock check_password from phpass.PasswordHash"""
    return password_1 == password_2


class ResponsesMixin(object):
    def setUp(self):
        assert responses, 'responses package required to use ResponsesMixin'
        responses.start()
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=43.69448&lon=6.85575',
                      status=200, body='FR')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=43.69448&lon=6.85575',
                      status=200, body='720')

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06453&lon=9.32880',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06255&lon=9.34737',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06313&lon=9.32412',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07567&lon=9.35367',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.08638&lon=9.50065',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07258&lon=9.35628',
                      status=200, body='DE')

        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06453&lon=9.32880',
                      status=200, body='79')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06255&lon=9.34737',
                      status=200, body='73')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06313&lon=9.32412',
                      status=200, body='84')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07567&lon=9.35367',
                      status=200, body='126')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.08638&lon=9.50065',
                      status=200, body='130')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07258&lon=9.35628',
                      status=200, body='154')

        super(ResponsesMixin, self).setUp()

    def tearDown(self):
        super(ResponsesMixin, self).tearDown()
        responses.stop()
        responses.reset()


class GeokretyTestCase(unittest.TestCase):
    def setUp(self):
        Setup.drop_db()
        self.app = Setup.create_app()
        phpass.PasswordHash.hash_password = mock_hash_password
        phpass.PasswordHash.check_password = mock_check_password

    def tearDown(self):
        Setup.drop_db()

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
              content_type='application/vnd.api+json'):
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
                                                 data=json.dumps(payload, default=json_serial),
                                                 headers=headers,
                                                 content_type=content_type)
        data = response.get_data(as_text=True)
        if response.status_code != code:  # pragma: no cover
            print("Endpoint: %s" % endpoint)
            pprint.pprint(json.dumps(payload, default=json_serial))
            pprint.pprint(data)
            pprint.pprint(payload)

        self.assertEqual(response.status_code, code)
        if response.content_type in ['application/vnd.api+json', 'application/json'] and data:
            return json.loads(data)
        return data

    def _send_post(self,
                   endpoint,
                   code=200,
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

    def assertDateTimeEqual(self, datetime_str, datetime_obj):
        if isinstance(datetime_obj, str):   # pragma: no cover
            # Check date is parsable
            raised = False
            try:
                datetime.strptime(datetime_obj, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                raised = True
            self.assertFalse(raised, 'Date is not parsable')
        else:
            self.assertEqual(datetime_str, datetime_obj.strftime("%Y-%m-%dT%H:%M:%S"))

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

    def _check_geokret(self, data, geokret, skip_check=None, with_private=False):
        skip_check = skip_check or []
        self.assertTrue('attributes' in data)
        attributes = data['attributes']

        self.assertTrue('name' in attributes)
        self.assertTrue('description' in attributes)
        self.assertTrue('missing' in attributes)
        self.assertTrue('distance' in attributes)
        self.assertTrue('caches-count' in attributes)
        self.assertTrue('pictures-count' in attributes)
        self.assertTrue('average-rating' in attributes)
        self.assertTrue('created-on-date-time' in attributes)
        self.assertTrue('updated-on-date-time' in attributes)

        self.assertEqual(attributes['name'], geokret.name)
        self.assertEqual(attributes['description'], geokret.description)
        self.assertEqual(attributes['missing'], geokret.missing)
        self.assertEqual(attributes['distance'], geokret.distance)
        self.assertEqual(attributes['caches-count'], geokret.caches_count)
        self.assertEqual(attributes['pictures-count'], geokret.pictures_count)
        self.assertEqual(attributes['average-rating'], geokret.average_rating)

        if 'times' not in skip_check:
            self.assertDateTimeEqual(attributes['created-on-date-time'], geokret.created_on_date_time)
            self.assertDateTimeEqual(attributes['updated-on-date-time'], geokret.updated_on_date_time)

        if with_private is not None:
            self.assertTrue('attributes' in data)
            attributes = data['attributes']

            self.assertTrue('tracking-code' in attributes)
            if with_private:
                if 'tracking-code' not in skip_check:
                    self.assertEqual(attributes['tracking-code'], geokret.tracking_code)
            else:
                self.assertIsNone(attributes['tracking-code'])

    def _check_move(self, data, move, skip_check=None):
        skip_check = skip_check or []
        self.assertTrue('attributes' in data)
        attributes = data['attributes']

        self.assertTrue('move-type-id' in attributes)
        self.assertTrue('altitude' in attributes)
        self.assertTrue('country' in attributes)
        self.assertTrue('distance' in attributes)
        self.assertTrue('comment' in attributes)
        self.assertTrue('username' in attributes)
        self.assertTrue('application-name' in attributes)
        self.assertTrue('application-version' in attributes)
        self.assertTrue('pictures-count' in attributes)
        self.assertTrue('comments-count' in attributes)
        self.assertTrue('moved-on-date-time' in attributes)
        self.assertTrue('created-on-date-time' in attributes)
        self.assertTrue('updated-on-date-time' in attributes)

        self.assertEqual(attributes['move-type-id'], move.move_type_id)
        self.assertEqual(attributes['altitude'], move.altitude)
        self.assertEqual(attributes['country'], move.country)
        self.assertEqual(attributes['distance'], move.distance)
        self.assertEqual(attributes['comment'], move.comment)
        self.assertEqual(attributes['username'], move.username)
        self.assertEqual(attributes['application-name'], move.application_name)
        self.assertEqual(attributes['application-version'], move.application_version)
        self.assertEqual(attributes['pictures-count'], move.pictures_count)
        self.assertEqual(attributes['comments-count'], move.comments_count)

        if attributes['moved-on-date-time'] is not None:
            self.assertDateTimeEqual(attributes['moved-on-date-time'], move.moved_on_date_time)

        if attributes['move-type-id'] in (MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN, MOVE_TYPE_DIPPED):
            self.assertTrue('latitude' in attributes)
            self.assertTrue('longitude' in attributes)
            self.assertTrue('waypoint' in attributes)
            self.assertEqual(attributes['latitude'], float(move.latitude))
            self.assertEqual(attributes['longitude'], float(move.longitude))
            self.assertEqual(attributes['waypoint'], move.waypoint)

        if 'times' not in skip_check:
            self.assertDateTimeEqual(attributes['created-on-date-time'], move.created_on_date_time)
            self.assertDateTimeEqual(attributes['updated-on-date-time'], move.updated_on_date_time)


class MovePayload(dict):
    def __init__(self, move_type, no_application_info=False):
        self.update({
            "data": {
                "type": "move",
                "attributes": {
                    "move_type_id": move_type,
                },
                "relationships": {}
            }
        })
        self.moved_date_time()
        self.application_name()
        self.application_version()

    def coordinates(self, latitude=43.78, longitude=7.06):
        self['data']['attributes']['latitude'] = latitude
        self['data']['attributes']['longitude'] = longitude
        return self

    def tracking_code(self, tracking_code="ABC123"):
        # if tracking_code is None:
        #     tracking_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        self['data']['attributes']['tracking_code'] = tracking_code
        return self

    def application_name(self, application_name="GeoKrety API"):
        self['data']['attributes']['application_name'] = application_name
        return self

    def application_version(self, application_version="Unit Tests 1.0"):
        self['data']['attributes']['application_version'] = application_version
        return self

    def comment(self, comment="Born here ;)"):
        self['data']['attributes']['comment'] = comment
        return self

    def moved_date_time(self, date_time=None):
        def random_date(start):
            """Generate a random datetime between `start` and `end`"""
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.utcnow()
            return (start + timedelta(
                # Get a random amount of seconds between `start` and `end`
                seconds=random.randint(0, int((end - start).total_seconds())),
            )).strftime("%Y-%m-%dT%H:%M:%S")

        if date_time:
            self['data']['attributes']['moved_on_date_time'] = date_time
        else:
            self['data']['attributes']['moved_on_date_time'] = random_date("2017-12-01T14:18:22")
        return self

    def username(self, username="Anyone"):
        self['data']['attributes']['username'] = username
        return self

    def author_id(self, author_id="0"):
        self['data']['attributes']['author_id'] = str(author_id)
        return self

    def author_relationship(self, user_id="0"):
        relationship_author = {
            "data": {
                "type": "user",
                "id": str(user_id)
            }
        }
        self['data']['relationships']['author'] = relationship_author
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            move = mixer.blend(Move)
            for key in self['data']['attributes'].keys():
                setattr(move, key, self['data']['attributes'][key])
            return move
