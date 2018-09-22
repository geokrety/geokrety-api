# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN,
                                         MOVE_TYPES_TEXT)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  request_context)
from tests.unittests.utils.responses.collections import \
    GeokretCollectionResponse


class TestGeokretyCollection(BaseTestCase):
    """Test Geokrety collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety?%s" % (args_)
        return GeokretCollectionResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    @request_context
    def test_geokret_collection_get_as_anonymous(self):
        geokrety = self.blend_geokret(owner=self.user_1, count=5)
        response = self.send_get(user=None)
        i = 0
        for geokret_response in response.data:
            geokret_response.assertHasPublicAttributes(geokrety[i])
            geokret_response.assertHasTrackingCode(None)
            i = i + 1

    @request_context
    def test_geokret_collection_as_administrator(self):
        geokrety = self.blend_geokret(owner=self.user_1, count=5)
        response = self.send_get(user=self.admin)
        i = 0
        for geokret_response in response.data:
            geokret_response.assertHasPublicAttributes(geokrety[i])
            geokret_response.assertHasTrackingCode(geokrety[i].tracking_code)
            i = i + 1

    @request_context
    def test_geokret_collection_as_authenticated(self):
        geokrety = self.blend_geokret(owner=self.user_1, count=5)
        response = self.send_get(user=self.user_2)
        i = 0
        for geokret_response in response.data:
            geokret_response.assertHasPublicAttributes(geokrety[i])
            geokret_response.assertHasTrackingCode(None)
            i = i + 1

    @request_context
    def test_geokret_collection_as_owner(self):
        geokret = self.blend_geokret(owner=self.user_2)
        geokrety = self.blend_geokret(owner=self.user_1, count=4)
        response = self.send_get(user=self.user_2)
        response.data[0].assertHasPublicAttributes(geokret)
        response.data[0].assertHasTrackingCode(geokret.tracking_code)
        for i in range(1, 5):
            response.data[i].assertHasPublicAttributes(geokrety[i - 1])
            response.data[i].assertHasTrackingCode(None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, True],
        [MOVE_TYPE_GRABBED, True],
        [MOVE_TYPE_COMMENT, False],
        [MOVE_TYPE_SEEN, True],
        [MOVE_TYPE_ARCHIVED, True],
        [MOVE_TYPE_DIPPED, True],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_geokret_collection_has_tracking_code_when_user_has_touched(self, input, expected):
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

    @parameterized.expand([
        [None, False],
        ['admin', True],
        ['user_1', True],  # Owner
        ['user_2', False],
    ])
    @request_context
    def test_geokret_collection_filter_by_tracking_code_as(self, input, expected):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(
            user=getattr(self, input) if input else None,
            args={'filter': '[{"name":"tracking_code","op":"eq","val":"%s"}]' % (geokret.tracking_code)}
        )
        if expected:
            response.data[0].assertHasTrackingCode(geokret.tracking_code)
        else:
            response.data[0].assertHasTrackingCode(None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, True],
        [MOVE_TYPE_GRABBED, True],
        [MOVE_TYPE_COMMENT, False],
        [MOVE_TYPE_SEEN, True],
        [MOVE_TYPE_ARCHIVED, True],
        [MOVE_TYPE_DIPPED, True],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_geokret_collection_filter_by_tracking_code_user_has_touched(self, input, expected):
        geokret = self.blend_geokret(author=self.user_2, created_on_datetime="2018-09-21T23:55:20")
        self.blend_move(geokret=geokret, author=self.user_1, move_type_id=input,
                        moved_on_datetime="2018-09-21T23:55:21")
        self.blend_move(geokret=geokret, author=self.user_2, move_type_id=MOVE_TYPE_GRABBED,
                        moved_on_datetime="2018-09-21T23:55:22")
        response = self.send_get(
            user=self.user_1,
            args={'filter': '[{"name":"tracking_code","op":"eq","val":"%s"}]' % (geokret.tracking_code)}
        )
        if expected:
            response.data[0].assertHasTrackingCode(geokret.tracking_code)
        else:
            response.data[0].assertHasTrackingCode(None)
