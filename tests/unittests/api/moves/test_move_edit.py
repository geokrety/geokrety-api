# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (MOVE_TYPE_COMMENT, MOVE_TYPE_DIPPED,
                                         MOVE_TYPE_DROPPED, MOVE_TYPE_GRABBED,
                                         MOVE_TYPE_SEEN)
from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.move import \
    MovePayload as MovePayloadOriginal
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.static_test_cases import (HTML_SUBSET_TEST_CASES,
                                                     UTF8_TEST_CASES)


class MovePayload(MovePayloadOriginal):
    def blend(self, *args, **kwargs):
        self.set_type(kwargs['type'])


class TestMoveEdit(BaseTestCase):
    """Test Move edit"""

    def send_patch(self, obj_id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/moves/%s?%s" % (obj_id, args_)
        return MoveResponse(self._send_patch(url, **kwargs).get_json())

    @parameterized.expand([
        [None, 401],
        ['admin', 200],  # Admin
        ['user_1', 200],  # Author
        ['user_2', 403],
        ['user_0', 200],  # GeoKret owner
    ])
    @request_context
    def test_moves_edit_is_forbidden_as(self, username, expected):
        self.user_0 = self.blend_user()
        geokret = self.blend_geokret(owner=self.user_0)
        move = self.blend_move(type=MOVE_TYPE_DIPPED, geokret=geokret, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .del_type()\
            .set_id(move.id)\
            .set_coordinates()\
            .set_comment("Some new comment")
        user = getattr(self, username) if username else None
        assert self.send_patch(move.id, payload=payload, user=user, code=expected)
        if expected == 200:
            self.assertEqual(move.comment, "Some new comment")
        else:
            self.assertNotEqual(move.comment, "Some new comment")

    @request_context
    def test_no_need_to_include_coordinates_if_last_move_has_coordinates(self):
        move = self.blend_move(type=MOVE_TYPE_DROPPED, latitude=43.78, longitude=7.06)
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_DIPPED)

    @request_context
    def test_must_include_coordinates_if_missing_from_last_move(self):
        move = self.blend_move(type=MOVE_TYPE_GRABBED)
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move.id)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')
        response.assertRaiseJsonApiError('/data/attributes/longitude')

        payload.set_coordinates()
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_DIPPED)

    @request_context
    def test_coordinates_are_optionnal_for_grab(self):
        move = self.blend_move(type=MOVE_TYPE_DIPPED)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_GRABBED)

        payload.set_coordinates()
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_GRABBED)

    @request_context
    def test_convert_to_dropped(self):
        move = self.blend_move(type=MOVE_TYPE_GRABBED)
        payload = MovePayload(MOVE_TYPE_DROPPED)\
            .set_id(move.id)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')
        response.assertRaiseJsonApiError('/data/attributes/longitude')

        payload.set_coordinates()
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_DROPPED)
        self.assertEqual(float(move.latitude), 43.78)
        self.assertEqual(float(move.longitude), 7.06)

    @request_context
    def test_convert_to_grabbed(self):
        move = self.blend_move(type=MOVE_TYPE_DROPPED, latitude=43.78, longitude=7.06)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_GRABBED)
        self.assertEqual(float(move.latitude), 43.78)
        self.assertEqual(float(move.longitude), 7.06)

        payload.set_coordinates(None, None)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_GRABBED)
        self.assertIsNone(move.latitude)
        self.assertIsNone(move.longitude)

    @request_context
    def test_convert_to_comment(self):
        move = self.blend_move(type=MOVE_TYPE_DROPPED, latitude=43.78, longitude=7.06)
        payload = MovePayload(MOVE_TYPE_COMMENT)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_COMMENT)
        self.assertIsNone(move.latitude)
        self.assertIsNone(move.longitude)

    @request_context
    def test_convert_to_seen(self):
        move = self.blend_move(type=MOVE_TYPE_DROPPED, latitude=43.78, longitude=7.06)
        payload = MovePayload(MOVE_TYPE_SEEN)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_SEEN)
        self.assertEqual(float(move.latitude), 43.78)
        self.assertEqual(float(move.longitude), 7.06)

        payload._set_attribute('latitude', 43.79)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_SEEN)
        self.assertEqual(float(move.latitude), 43.79)
        self.assertEqual(float(move.longitude), 7.06)

        payload.set_coordinates(None, None)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @request_context
    def test_convert_to_dipped(self):
        move = self.blend_move(type=MOVE_TYPE_DROPPED, latitude=43.78, longitude=7.06)
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move.id)
        assert self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_DIPPED)
        self.assertEqual(float(move.latitude), 43.78)
        self.assertEqual(float(move.longitude), 7.06)

        payload.set_coordinates(None, None)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/latitude')
        response.assertRaiseJsonApiError('/data/attributes/longitude')

    @request_context
    def test_author_change_restrictions(self):
        move = self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)\
            .set_author(self.user_2.id)
        response = self.send_patch(move.id, payload=payload, user=self.user_1, code=403)
        response.assertRaiseJsonApiError('/data/relationships/author')

        response = self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.author.id, self.user_2.id)

    @request_context
    def test_geokret_relation_can_be_changed_only_by_admin(self):
        geokret = self.blend_geokret()
        move = self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)\
            .set_geokret(geokret.id)
        response = self.send_patch(move.id, payload=payload, user=self.user_1, code=403)
        response.assertRaiseJsonApiError('/data/relationships/geokret')

        response = self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.geokret.id, geokret.id)

    @request_context
    def test_from_non_authenticated_move_type_need_tracking_code(self):
        move = self.blend_move(type=MOVE_TYPE_COMMENT)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=422)
        response.assertRaiseJsonApiError('/data/attributes/tracking-code')

        payload.set_tracking_code(move.geokret.tracking_code)
        response = self.send_patch(move.id, payload=payload, user=self.admin, code=200)
        self.assertEqual(move.type, MOVE_TYPE_GRABBED)

    @request_context
    def test_geokret_can_be_changed_via_tracking_code(self):
        geokret = self.blend_geokret()
        move = self.blend_move(type=MOVE_TYPE_GRABBED, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)\
            .set_tracking_code(geokret.tracking_code)
        response = self.send_patch(move.id, payload=payload, user=self.user_1, code=200)
        response.assertHasRelationshipGeokretData(geokret.id)

    @request_context
    def test_move_datetime_cannot_be_before_geokret_birth(self):
        geokret = self.blend_geokret(created_on_datetime='2018-12-28T15:25:56')
        move = self.blend_move(type=MOVE_TYPE_GRABBED, geokret=geokret, author=self.user_1)

        payload = MovePayload(MOVE_TYPE_GRABBED)\
            .set_id(move.id)\
            .set_moved_on_datetime('2018-12-28T14:00:00')
        response = self.send_patch(move.id, payload=payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

        payload.set_moved_on_datetime(geokret.created_on_datetime)
        response = self.send_patch(move.id, payload=payload, user=self.user_1, code=200)

    @request_context
    def test_move_datetime_same_as_another_move(self):
        geokret = self.blend_geokret(created_on_datetime='2018-12-28T16:26:16')
        move_1 = self.blend_move(type=MOVE_TYPE_GRABBED, geokret=geokret,
                                 author=self.user_1, moved_on_datetime='2018-12-28T16:26:49')
        move_2 = self.blend_move(type=MOVE_TYPE_GRABBED, geokret=geokret,
                                 author=self.user_1, moved_on_datetime='2018-12-28T16:26:58')

        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move_2.id)\
            .set_coordinates()\
            .set_moved_on_datetime(move_2.moved_on_datetime)
        self.send_patch(move_2.id, payload=payload, user=self.user_1)

        payload.set_moved_on_datetime(move_1.moved_on_datetime)
        response = self.send_patch(move_2.id, payload=payload, user=self.user_1, code=422)
        response.assertRaiseJsonApiError('/data/attributes/moved-on-datetime')

    @parameterized.expand(HTML_SUBSET_TEST_CASES)
    @request_context
    def test_move_field_comment_accept_html_subset(self, comment, expected):
        geokret = self.blend_geokret()
        move = self.blend_move(type=MOVE_TYPE_GRABBED, geokret=geokret, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_id(move.id)
        payload.set_comment(comment)
        response = self.send_patch(move.id, payload=payload, user=self.user_1)
        response.assertHasAttribute('comment', expected)

    @parameterized.expand(UTF8_TEST_CASES)
    @request_context
    def test_move_field_comment_accept_unicode(self, comment, expected):
        geokret = self.blend_geokret()
        move = self.blend_move(type=MOVE_TYPE_GRABBED, geokret=geokret, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_id(move.id)
        payload.set_comment(comment)
        response = self.send_patch(move.id, payload=payload, user=self.user_1)
        response.assertHasAttribute('comment', expected)

    @request_context
    def test_altitude_and_country_is_computed_and_not_overridable(self):
        geokret = self.blend_geokret()
        move = self.blend_move(type=MOVE_TYPE_GRABBED,
                               geokret=geokret, author=self.user_1)
        payload = MovePayload(MOVE_TYPE_GRABBED, geokret=geokret)\
            .set_id(move.id)\
            .set_coordinates(52.07567, 9.35367)
        payload._set_attribute('altitude', 666)
        payload._set_attribute('country', 'PL')
        response = self.send_patch(move.id, payload=payload, user=self.user_1)
        response.assertHasAttribute('altitude', 126)
        response.assertHasAttribute('country', 'DE')

    @request_context
    def test_distance_is_reevaluated_for_new_and_old_geokrety(self):
        geokret_1 = self.blend_geokret(created_on_datetime='2018-12-29T10:52:00')
        geokret_2 = self.blend_geokret(created_on_datetime='2018-12-29T10:52:00')

        self.blend_move(type=MOVE_TYPE_DIPPED, geokret=geokret_1,
                        author=self.user_1,
                        latitude=43.704233, longitude=6.869833,
                        moved_on_datetime='2018-12-29T10:52:06')
        self.blend_move(type=MOVE_TYPE_DIPPED, geokret=geokret_2,
                        author=self.user_1,
                        latitude=43.704233, longitude=6.869833,
                        moved_on_datetime='2018-12-29T10:52:06')

        move = self.blend_move(type=MOVE_TYPE_DIPPED, geokret=geokret_1,
                               author=self.user_1,
                               latitude=43.6792, longitude=6.852933,
                               moved_on_datetime='2018-12-29T10:52:22')

        # Change coordinates
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move.id)\
            .set_coordinates(52.07567, 9.35367)
        response = self.send_patch(move.id, payload=payload, user=self.user_1)
        response.assertHasAttribute('distance', 949)
        self.assertEqual(geokret_1.distance, 949)

        # Change GeoKret
        payload = MovePayload(MOVE_TYPE_DIPPED)\
            .set_id(move.id)\
            .set_tracking_code(geokret_2.tracking_code)
        response = self.send_patch(move.id, payload=payload, user=self.user_1)
        response.assertHasAttribute('distance', 949)
        self.assertEqual(geokret_1.distance, 0)
        self.assertEqual(geokret_2.distance, 949)
