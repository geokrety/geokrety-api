# -*- coding: utf-8 -*-

import urllib
from datetime import datetime, timedelta

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED)
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import MovePayload
from tests.unittests.utils.responses.collections import \
    GeokretCollectionResponse
from tests.unittests.utils.responses.move import MoveResponse


class TestMoveCreateArchive(BaseTestCase):
    """Test Move create Archive"""

    def send_post(self, payload=None, code=201, user=None, content_type='application/vnd.api+json'):
        return MoveResponse(super(TestMoveCreateArchive, self)._send_post(
            "/v1/moves",
            code=code,
            payload=payload,
            user=user,
            content_type=content_type).get_json())

    def send_get_gk_collection(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety?%s" % (args_)
        return GeokretCollectionResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        ['user_1'],
        ['user_2'],
    ])
    @request_context
    def test_move_create_archive_as(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret()
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)
        assert self.send_post(payload, user=user, code=403)

    @parameterized.expand([
        ['user_1'],
        ['admin'],
    ])
    @request_context
    def test_move_create_archive_as_owner(self, username):
        user = getattr(self, username) if username else None
        geokret = self.blend_geokret(owner=self.user_1)
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)
        self.send_post(payload, user=user, code=201)
        self.assertEqual(geokret.archived, True)

    @request_context
    def test_archive_date_must_be_provided(self):
        geokret = self.blend_geokret(owner=self.user_1)
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)
        payload['data']['attributes'].pop('moved-on-datetime')
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @request_context
    def test_archive_date_must_not_be_before_born_date(self):
        geokret = self.blend_geokret(owner=self.user_1, created_on_datetime='2018-12-29T16:33:46')
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)\
            .set_moved_on_datetime('2018-12-29T16:33:00')
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @request_context
    def test_archive_date_must_not_be_the_future(self):
        geokret = self.blend_geokret(owner=self.user_1)
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)\
            .set_moved_on_datetime(datetime.now() + timedelta(hours=6))
        response = self.send_post(payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @request_context
    def test_a_comment_may_be_provided(self):
        geokret = self.blend_geokret(owner=self.user_1)
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)\
            .set_comment("Some comment")
        self.send_post(payload, user=self.user_1)

    @request_context
    def test_moves_can_continue_after_archive(self):
        geokret = self.blend_geokret(owner=self.user_1, created_on_datetime='2018-12-29T16:40:06')
        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret)\
            .set_moved_on_datetime('2018-12-29T16:40:14')
        self.send_post(payload, user=self.user_1)
        self.assertTrue(geokret.archived)
        payload = MovePayload(MOVE_TYPE_COMMENT, geokret=geokret)\
            .set_moved_on_datetime('2018-12-29T16:40:33')\
            .set_comment("This GeoKret is not dead")
        self.send_post(payload, user=self.user_1)
        self.assertTrue(geokret.archived)
        payload = MovePayload(MOVE_TYPE_DIPPED, geokret=geokret)\
            .set_moved_on_datetime('2018-12-29T16:40:41')\
            .set_coordinates()\
            .set_comment("Will continue it's journey")
        self.send_post(payload, user=self.user_1)
        self.assertFalse(geokret.archived)

    @request_context
    def test_archived_geokret_must_not_be_shown_in_cache_details(self):
        geokret_1 = self.blend_geokret(owner=self.user_1, created_on_datetime='2018-12-29T16:43:28')
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret_1)\
            .set_moved_on_datetime('2018-12-29T16:44:57')\
            .set_coordinates()\
            .set_waypoint('ABC123')
        self.send_post(payload, user=self.user_1)

        geokret_2 = self.blend_geokret(owner=self.user_1, created_on_datetime='2018-12-29T16:43:28')
        payload = MovePayload(MOVE_TYPE_DROPPED, geokret=geokret_2)\
            .set_moved_on_datetime('2018-12-29T16:44:57')\
            .set_coordinates()\
            .set_waypoint('ABC123')
        self.send_post(payload, user=self.user_1)

        response = self.send_get_gk_collection(
            args={'filter': '[{"name":"last_position","op":"has","val":{"name":"waypoint","op":"eq","val":"ABC123"}}]'})
        response.assertCount(2)

        payload = MovePayload(MOVE_TYPE_ARCHIVED, geokret=geokret_1)\
            .set_moved_on_datetime('2018-12-29T16:45:03')
        response = self.send_get_gk_collection(
            args={'filter': '[{"name":"last_position__waypoint","op":"has","val":"ABC123"}]'})
        response.assertCount(2)
