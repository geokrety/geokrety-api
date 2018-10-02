# -*- coding: utf-8 -*-

import urllib

from flask_rest_jsonapi.exceptions import ObjectNotFound
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.db import safe_query
from app.models.user import User
from tests.unittests.utils.base_test_case import (BaseTestCase, request_context)
from tests.unittests.utils.payload.user import UserPayload
from tests.unittests.utils.responses.collections import UsersCollectionResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestUsersCollection(BaseTestCase):
    """Test Users collection"""

    def send_get(self, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/users?%s" % (args_)
        return UsersCollectionResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    @request_context
    def test_user_details_has_public_attributes_as_anonymous_user(self):
        response = self.send_get()
        response.assertCount(3)
        response.data[0].assertHasPublicAttributes(self.admin)
        response.data[1].assertHasPublicAttributes(self.user_1)
        response.data[2].assertHasPublicAttributes(self.user_2)

    @request_context
    def test_user_details_has_public_attributes_as_authenticated_user(self):
        response = self.send_get(user=self.user_2)
        response.assertCount(3)
        response.data[0].assertHasPublicAttributes(self.admin)
        response.data[1].assertHasPublicAttributes(self.user_1)
        response.data[2].assertHasPrivateAttributes(self.user_2)

    @request_context
    def test_user_details_has_private_attributes_as_admin(self):
        response = self.send_get(user=self.admin)
        response.assertCount(3)
        response.data[0].assertHasPrivateAttributes(self.admin)
        response.data[1].assertHasPrivateAttributes(self.user_1)
        response.data[2].assertHasPrivateAttributes(self.user_2)
