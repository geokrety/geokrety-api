# -*- coding: utf-8 -*-

from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import MOVE_TYPE_GRABBED
from tests.unittests.utils.base_test_case import (BaseTestCase)
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
            self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=None)
            for geokret_response in response.data:
                geokret_response.assertHasTrackingCode(None)

    def test_get_collection_as_administrator(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=self.admin)
            i = 0
            for geokret_response in response.data:
                geokret_response.assertHasTrackingCode(geokret[i].tracking_code)
                i = i + 1

    def test_get_collection_as_authenticated(self):
        with app.test_request_context():
            self.blend_users()
            user_2 = self.blend_user()
            self.blend_geokret(owner=self.user_1, count=5)
            response = self.send_get(user=user_2)
            for geokret_response in response.data:
                geokret_response.assertHasTrackingCode(None)

    def test_get_collection_as_owner(self):
        with app.test_request_context():
            self.blend_users()
            user_2 = self.blend_user()
            geokret = self.blend_geokret(owner=user_2)
            self.blend_geokret(owner=self.user_1, count=4)
            response = self.send_get(user=user_2)
            response.data[0].assertHasTrackingCode(geokret.tracking_code)
            for i in range(1, 5):
                response.data[i].assertHasTrackingCode(None)
