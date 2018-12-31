# -*- coding: utf-8 -*-

from tests.unittests.utils.base_test_case import BaseTestCase, request_context
from tests.unittests.utils.payload.user import UserPayload


class TestUsersCollection(BaseTestCase):
    """Test Users collection"""

    @request_context
    def test_user_details_has_public_attributes_as_anonymous_user(self):
        response = UserPayload()\
            .get_collection()\
            .assertCount(3)
        response.data[0].assertHasPublicAttributes(self.admin)
        response.data[1].assertHasPublicAttributes(self.user_1)
        response.data[2].assertHasPublicAttributes(self.user_2)

    @request_context
    def test_user_details_has_public_attributes_as_authenticated_user(self):
        response = UserPayload()\
            .get_collection(user=self.user_2)\
            .assertCount(3)
        response.data[0].assertHasPublicAttributes(self.admin)
        response.data[1].assertHasPublicAttributes(self.user_1)
        response.data[2].assertHasPrivateAttributes(self.user_2)

    @request_context
    def test_user_details_has_private_attributes_as_admin(self):
        response = UserPayload()\
            .get_collection(user=self.admin)\
            .assertCount(3)
        response.data[0].assertHasPrivateAttributes(self.admin)
        response.data[1].assertHasPrivateAttributes(self.user_1)
        response.data[2].assertHasPrivateAttributes(self.user_2)
