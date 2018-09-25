# -*- coding: utf-8 -*-

import urllib

from flask_rest_jsonapi.exceptions import ObjectNotFound
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN,
                                         MOVE_TYPES_TEXT)
from app.api.helpers.db import safe_query
from app.models.move import Move
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_type,
                                                  request_context)
from tests.unittests.utils.responses.geokrety_types import \
    GeokretyTypesResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class fakeGeokretyType(object):
    def __init__(self, name):
        self.name = name


class TestGeokretyTypeDetails(BaseTestCase):
    """Test GeoKrety details"""

    def send_get(self, id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety-types/%s?%s" % (id, args_)
        return GeokretyTypesResponse(self._send_get(url, **kwargs).get_json())

    @parameterized.expand([
        [GEOKRET_TYPE_TRADITIONAL, "Traditional"],
        [GEOKRET_TYPE_BOOK, "A book/CD/DVD"],
        [GEOKRET_TYPE_HUMAN, "A Human"],
        [GEOKRET_TYPE_COIN, "A coin"],
        [GEOKRET_TYPE_KRETYPOST, "KretyPost"],
    ], doc_func=custom_name_geokrety_type)
    @request_context
    def test_geokrety_types_details_has_normal_attributes_as_anonymous_user(self, input, expected):
        fake_type = fakeGeokretyType(expected)
        response = self.send_get(input)
        response.assertHasPublicAttributes(fake_type)
