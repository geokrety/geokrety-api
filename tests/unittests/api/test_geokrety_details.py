# -*- coding: utf-8 -*-

from flask_rest_jsonapi.exceptions import ObjectNotFound
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TEXT,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_DIPPED)
from app.api.helpers.db import safe_query
from app.models.move import Move
from tests.unittests.utils.base_test_case import BaseTestCase
from tests.unittests.utils.payload.geokret import GeokretyPayload
from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestGeokretDetails(BaseTestCase):
    """Test Geokrety details"""

    def send_get(self, id, include=None, **kwargs):
        url = "/v1/geokrety/%s" % id
        print url
        if include:
            url = "%s?include=%s" % (url, ','.join(include))
        return GeokretResponse(self._send_get(url, **kwargs))

    # ## TEST CASES ##

    def test_has_tracking_code_as_anonymous_user(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret()
            response = self.send_get(geokret.id, user=None)
            response.assertHasPublicAttributes(geokret)
            response.assertHasAttribute('tracking-code', None)

    def test_has_tracking_code_as_authenticated_user(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.admin)
            response = self.send_get(geokret.id, user=self.user_1)
            response.assertHasPublicAttributes(geokret)
            response.assertHasAttribute('tracking-code', None)

    def test_has_tracking_code_as_owner(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_1)
            response = self.send_get(geokret.id, user=self.user_1)
            response.assertHasPublicAttributes(geokret)
            response.assertHasAttribute('tracking-code', geokret.tracking_code)

    def test_has_tracking_code_as_holder(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(holder=self.user_1)
            response = self.send_get(geokret.id, user=self.user_1)
            response.assertHasPublicAttributes(geokret)
            response.assertHasAttribute('tracking-code', geokret.tracking_code)

    def test_has_tracking_code_as_admin_user(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_1)
            response = self.send_get(geokret.id, user=self.admin)
            response.assertHasPublicAttributes(geokret)
            response.assertHasAttribute('tracking-code', geokret.tracking_code)

    def test_has_relationships_owner_data(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(owner=self.user_1)
            response = self.send_get(geokret.id, user=None)
            response.assertHasRelationshipData('owner', geokret.owner_id, 'user')
            with self.assertRaises(AssertionError):
                response.assertHasRelationshipData('holder', geokret.holder_id, 'user')

    def test_has_relationships_holder_data(self):
        with app.test_request_context():
            self.blend_users()
            geokret = self.blend_geokret(holder=self.user_2)
            response = self.send_get(geokret.id, user=None)
            with self.assertRaises(AssertionError):
                response.assertHasRelationshipData('owner', geokret.owner_id, 'user')
            response.assertHasRelationshipData('holder', geokret.holder_id, 'user')
