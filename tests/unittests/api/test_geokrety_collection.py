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
from tests.unittests.utils.responses.collections import \
    GeokretCollectionResponse


class TestGeokretyCollection(BaseTestCase):
    """Test Geokrety collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety?%s" % (args_)
        print "URL: {}".format(url)
        return GeokretCollectionResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    def test_get_collection_as_anonymous(self):
        with app.test_request_context():
            self.blend_users()
            geokrety = self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=None)
            i = 0
            for geokret_response in response.data:
                geokret_response.assertHasPublicAttributes(geokrety[i])
                geokret_response.assertHasTrackingCode(None)
                i = i + 1

    def test_get_collection_as_administrator(self):
        with app.test_request_context():
            self.blend_users()
            geokrety = self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=self.admin)
            i = 0
            for geokret_response in response.data:
                geokret_response.assertHasPublicAttributes(geokrety[i])
                geokret_response.assertHasTrackingCode(geokrety[i].tracking_code)
                i = i + 1

    def test_get_collection_as_authenticated(self):
        with app.test_request_context():
            self.blend_users()
            geokrety = self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=self.user_2)
            i = 0
            for geokret_response in response.data:
                geokret_response.assertHasPublicAttributes(geokrety[i])
                geokret_response.assertHasTrackingCode(None)
                i = i + 1

    def test_get_collection_as_owner(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_2)
            geokrety = self.blend_geokret(owner=self.user_1, count=4)
            response = self.send_get(user=self.user_2)
            response.data[0].assertHasPublicAttributes(geokret)
            response.data[0].assertHasTrackingCode(geokret.tracking_code)
            for i in range(1, 5):
                response.data[i].assertHasPublicAttributes(geokrety[i-1])
                response.data[i].assertHasTrackingCode(None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, True],
        [MOVE_TYPE_GRABBED, True],
        [MOVE_TYPE_COMMENT, False],
        [MOVE_TYPE_SEEN, True],
        [MOVE_TYPE_ARCHIVED, True],
        [MOVE_TYPE_DIPPED, True],
    ], doc_func=custom_name_geokrety_move_type)
    def test_has_tracking_code_when_user_has_touched(self, input, expected):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(created_on_datetime="2018-09-20T23:15:30")
            self.blend_move(geokret=geokret, author=self.user_1, move_type_id=input,
                            moved_on_datetime="2018-09-20T23:15:31")
            self.blend_move(geokret=geokret, author=self.user_2, move_type_id=MOVE_TYPE_GRABBED,
                            moved_on_datetime="2018-09-20T23:15:32")
            response = self.send_get(user=self.user_1)
            if expected:
                response.data[0].assertHasTrackingCode(geokret.tracking_code)
            else:
                response.data[0].assertHasTrackingCode(None)
