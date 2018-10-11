# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_move_type,
                                                  custom_name_geokrety_type,
                                                  request_context)
from tests.unittests.utils.payload.geokret import GeokretyPayload
from tests.unittests.utils.responses.collections import GeokretResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES)


class TestGeokretyEdit(BaseTestCase):
    """Test edit Geokrety"""

    def send_patch(self, obj_id, payload, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety/%s?%s" % (obj_id, args_)
        payload.set_id(obj_id)
        return GeokretResponse(self._send_patch(url, payload=payload, **kwargs).get_json())

    #

    @request_context
    def test_geokret_patch_as_anonymous(self):
        geokret = self.blend_geokret()
        self.send_patch(geokret.id, GeokretyPayload(), user=None, code=401)

    @parameterized.expand([
        ['admin', True],
        ['user_1', True],  # Owner
        ['user_2', False],
    ])
    @request_context
    def test_geokret_patch_as(self, username, expected):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        geokret = self.blend_geokret(owner=self.user_1)
        user = getattr(self, username)
        if expected:
            response = self.send_patch(geokret.id, payload, user=self.admin, code=200)
            self.assertEqual(response.name, new_name)
        else:
            assert self.send_patch(geokret.id, payload, user=user, code=403)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED],
        [MOVE_TYPE_GRABBED],
        [MOVE_TYPE_COMMENT],
        [MOVE_TYPE_SEEN],
        [MOVE_TYPE_ARCHIVED],
        [MOVE_TYPE_DIPPED],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_geokret_patch_when_user_has_touched(self, move_type):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        geokret = self.blend_geokret(created_on_datetime="2018-09-22T18:18:55")
        self.blend_move(geokret=geokret, author=self.user_1,
                        type=move_type,
                        moved_on_datetime="2018-09-22T18:18:56")
        self.blend_move(geokret=geokret, author=self.user_2,
                        type=MOVE_TYPE_GRABBED,
                        moved_on_datetime="2018-09-22T18:18:57")
        self.send_patch(geokret.id, payload, user=self.user_1, code=403)

    @request_context
    def test_geokret_patch_field_name(self):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_patch(geokret.id, payload, user=self.user_1, code=200)
        self.assertEqual(response.name, new_name)

    @parameterized.expand(EMPTY_TEST_CASES)
    @request_context
    def test_geokret_patch_field_name_cannot_be_blank(self, name):
        payload = GeokretyPayload()
        payload.set_name(name)
        geokret = self.blend_geokret()
        response = self.send_patch(geokret.id, payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/name')

    @parameterized.expand(NO_HTML_TEST_CASES)
    @request_context
    def test_geokret_patch_field_name_doesnt_accept_html(self, name, result=None):
        payload = GeokretyPayload()
        payload.set_name(name)
        result = name if result is None else result
        geokret = self.blend_geokret()
        response = self.send_patch(geokret.id, payload, user=self.admin, code=200)
        self.assertEqual(response.name, result)

    @request_context
    def test_geokret_patch_field_description(self):
        payload = GeokretyPayload()
        new_description = 'some other description'
        payload._set_attribute('description', new_description)
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_patch(geokret.id, payload, user=self.user_1, code=200)
        self.assertEqual(response.description, new_description)

    @parameterized.expand(HTML_SUBSET_TEST_CASES)
    @request_context
    def test_geokret_patch_field_description_accept_html_subset(self, description, result=None):
        payload = GeokretyPayload()
        payload.set_description(description)
        result = description if result is None else result
        geokret = self.blend_geokret()
        response = self.send_patch(geokret.id, payload, user=self.admin, code=200)
        self.assertEqual(response.description, result)

    @parameterized.expand([
        ['admin', GEOKRET_TYPE_COIN, True],
        ['admin', GEOKRET_TYPE_TRADITIONAL, True],
        ['admin', GEOKRET_TYPE_BOOK, True],
        ['admin', GEOKRET_TYPE_HUMAN, True],
        ['admin', GEOKRET_TYPE_COIN, True],
        ['admin', GEOKRET_TYPE_KRETYPOST, True],
        ['admin', "non-existent", False],
        ['user_1', GEOKRET_TYPE_COIN, True],
        ['user_1', GEOKRET_TYPE_TRADITIONAL, True],
        ['user_1', GEOKRET_TYPE_BOOK, True],
        ['user_1', GEOKRET_TYPE_HUMAN, True],
        ['user_1', GEOKRET_TYPE_COIN, True],
        ['user_1', GEOKRET_TYPE_KRETYPOST, True],
        ['user_1', "non-existent", False],
    ], doc_func=custom_name_geokrety_type)
    @request_context
    def test_geokret_patch_field_type(self, input_user, input_type, expected):
        payload = GeokretyPayload()
        payload._set_relationships('type', 'type', input_type)
        user = getattr(self, input_user)
        geokret = self.blend_geokret(owner=self.user_1, type=GEOKRET_TYPE_TRADITIONAL)
        if expected:
            response = self.send_patch(geokret.id, payload, user=user, code=200)
            self.assertEqual(response.type, input_type)
        else:
            response = self.send_patch(geokret.id, payload, user=user, code=422)

    @request_context
    def test_geokret_patch_field_dump_only(self):
        payload = GeokretyPayload()
        payload._set_attribute('missing', True)
        payload._set_attribute('distance', 1000)
        payload._set_attribute('caches_count', 1000)
        payload._set_attribute('pictures_count', 1000)
        payload._set_attribute('average_rating', 1000)
        payload._set_attribute('created_on_datetime', "2018-09-22T19:38:28")
        payload._set_attribute('updated_on_datetime', "2018-09-22T19:38:29")
        geokret = self.blend_geokret(
            owner=self.user_1,
            missing=False,
            distance=12,
            caches_count=12,
            pictures_count=12,
            created_on_datetime="2018-09-22T19:34:41",
            updated_on_datetime="2018-09-22T19:34:42",
        )
        response = self.send_patch(geokret.id, payload, user=self.user_1, code=200)
        self.assertEqual(response.missing, geokret.missing)
        self.assertEqual(response.distance, geokret.distance)
        self.assertEqual(response.caches_count, geokret.caches_count)
        self.assertEqual(response.pictures_count, geokret.pictures_count)
        self.assertEqual(response.average_rating, geokret.average_rating)
        self.assertEqual(response.created_on_datetime, geokret.created_on_datetime)
        self.assertEqual(response.updated_on_datetime, geokret.updated_on_datetime)

    @request_context
    def test_geokret_patch_field_updated_on_datetime_automatically_changed(self):
        payload = GeokretyPayload()
        new_name = 'some other name'
        payload._set_attribute('name', new_name)
        geokret = self.blend_geokret(owner=self.user_1, updated_on_datetime="2018-09-22T20:27:08")
        updated_on_datetime = geokret.updated_on_datetime
        response = self.send_patch(geokret.id, payload, user=self.user_1, code=200)
        response.pprint()
        self.assertEqual(response.name, new_name)
        self.assertNotEqual(response.updated_on_datetime, updated_on_datetime)

    @request_context
    def test_geokret_patch_relationships_owner_as_admin(self):
        payload = GeokretyPayload()
        payload._set_relationships('owner', 'user', self.user_2.id)
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_patch(geokret.id, payload, user=self.admin)
        response.assertHasRelationshipOwnerData(self.user_2.id)

    @request_context
    def test_geokret_patch_relationships_owner_as_owner(self):
        payload = GeokretyPayload()
        payload._set_relationships('owner', 'user', self.user_2.id)
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_patch(geokret.id, payload, user=self.user_1)
        response.assertHasRelationshipOwnerData(self.user_1.id)

    @request_context
    def test_geokret_patch_relationships_owner_as_authenticated(self):
        payload = GeokretyPayload()
        payload._set_relationships('owner', 'user', self.user_2.id)
        geokret = self.blend_geokret(owner=self.user_1)
        self.send_patch(geokret.id, payload, user=self.user_2, code=403)

    @parameterized.expand([
        ['admin'],
        ['user_1'],  # Owner
    ])
    @request_context
    def test_geokret_patch_relationships_holder_as(self, username):
        payload = GeokretyPayload()
        payload._set_relationships('holder', 'user', self.user_2.id)
        geokret = self.blend_geokret(owner=self.user_1, holder=self.user_1)
        user = getattr(self, username) if username else None
        response = self.send_patch(geokret.id, payload, user=user)
        response.assertHasRelationshipHolderData(self.user_1.id)

    @parameterized.expand([
        ['admin'],
        ['user_1'],  # Owner
    ])
    @request_context
    def test_geokret_patch_relationships_moves_as(self, username):
        payload = GeokretyPayload()
        geokret_1 = self.blend_geokret(owner=self.user_1, holder=self.user_1)
        geokret_2 = self.blend_geokret()
        moves = self.blend_move(geokret=geokret_2, count=2)
        moves_ids = [move.id for move in moves]
        payload._set_relationships_many('moves', 'move', moves_ids)

        user = getattr(self, username) if username else None
        response = self.send_patch(geokret_1.id, payload, user=user, args={'include': 'moves'})
        response.assertHasRelationshipMovesDatas([])
