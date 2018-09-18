# -*- coding: utf-8 -*-

import pprint

from tests.unittests.utils import assertIsDateTime


class BaseResponse(dict):

    def __init__(self, data):
        self.update(data.get_json())

    @property
    def id(self):
        try:
            assert 'data' in self
            assert 'id' in self['data']
            return self['data']['id']
        except AssertionError:
            pprint.pprint(self)
            raise AttributeError("Object id not found in response.")

    def _get_attribute(self, attribute):
        try:
            assert 'data' in self
            assert 'attributes' in self['data']
            assert attribute in self['data']['attributes']
            return self['data']['attributes'][attribute]
        except AssertionError:
            pprint.pprint(self)
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def assertHasRelationship(self, response, relation_type, link):
        """Assert an error response has a specific pointer
        """
        if not isinstance(response, dict):
            raise TypeError("'response' parameter must be of type dict (%s)" % type(response))

        try:
            assert 'data' in response
            assert 'relationships' in response['data']
            assert relation_type in response['data']['relationships']
            assert 'links' in response['data']['relationships'][relation_type]
            assert 'related' in response['data']['relationships'][relation_type]['links']
            assert link in response['data']['relationships'][relation_type]['links']['related']
        except AssertionError:
            pprint.pprint(response)
            raise AttributeError("Link '%s' not found in relationship '%s'" % (link, relation_type))

    def assertHasAttribute(self, response, attribute, value):
        """Assert a response attribute has a specific value
        """
        if not isinstance(response, dict):
            raise TypeError("'response' parameter must be of type dict (%s)" % type(response))

        try:
            assert 'data' in response
            assert 'attributes' in response['data']
            assert attribute in response['data']['attributes']
            assert response['data']['attributes'][attribute] == value
        except AssertionError:
            pprint.pprint(response)
            raise

    def assertHasIncludeId(self, response, relationships, value):
        """Assert a response relation has a specific value
        """
        if not isinstance(response, dict):
            raise TypeError("'response' parameter must be of type dict (%s)" % type(response))

        try:
            assert 'data' in response
            assert 'relationships' in response['data']
            assert relationships in response['data']['relationships']
            assert 'data' in response['data']['relationships'][relationships]
            assert response['data']['relationships'][relationships]['data'] is not None
            assert 'id' in response['data']['relationships'][relationships]['data']
            assert response['data']['relationships'][relationships]['data']['id'] == str(value)
        except AssertionError:
            pprint.pprint(response)
            raise

    def assertHasIncludes(self, response, relationships, value):
        raise Unimplemented("Function assertHasIncludes is not yet implemented")

    def assertCreationDateTime(self, response):
        self.assertDateTimePresent(response, 'created-on-datetime')

    def assertUpdatedDateTime(self, response):
        self.assertDateTimePresent(response, 'updated-on-datetime')

    def assertDateTimePresent(self, response, attribute):
        if not isinstance(response, dict):
            raise TypeError("'response' parameter must be of type dict (%s)" % type(response))

        try:
            assert 'data' in response
            assert 'attributes' in response['data']
            assert attribute in response['data']['attributes']
            date_time = response['data']['attributes'][attribute]
            assertIsDateTime(date_time)
        except AssertionError:
            pprint.pprint(response)
            raise

    def assertRaiseJsonApiError(self, response, pointer):
        """Assert an error response has a specific pointer
        """
        if not isinstance(response, dict):
            raise TypeError("'response' parameter must be of type dict (%s)" % type(response))

        try:
            assert 'errors' in response
            for error in response['errors']:
                assert 'source' in error
                assert 'pointer' in error['source']
                if pointer in error['source']['pointer']:
                    return True
        except AssertionError:
            pprint.pprint(response)
            raise
