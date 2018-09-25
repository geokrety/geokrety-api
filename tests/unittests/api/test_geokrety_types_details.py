# -*- coding: utf-8 -*-

import urllib

from parameterized import parameterized

from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TRADITIONAL)
from tests.unittests.utils.base_test_case import (BaseTestCase,
                                                  custom_name_geokrety_type,
                                                  request_context)
from tests.unittests.utils.responses.geokrety_types import \
    GeokretyTypesResponse


class fakeGeokretyType(object):
    def __init__(self, name):
        self.name = name


class TestGeokretyTypeDetails(BaseTestCase):
    """Test GeoKrety Types details"""

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
