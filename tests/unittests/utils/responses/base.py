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
            self.pprint(self)
            raise AttributeError("Object id not found in response.")

    def _get_attribute(self, attribute):
        try:
            assert 'data' in self
            assert 'attributes' in self['data']
            assert attribute in self['data']['attributes']
            return self['data']['attributes'][attribute]
        except AssertionError:
            self.pprint(self)
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def assertHasRelationship(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        try:
            assert 'data' in self
            assert 'relationships' in self['data']
            assert relation_type in self['data']['relationships']
            assert 'links' in self['data']['relationships'][relation_type]
            assert 'related' in self['data']['relationships'][relation_type]['links']
            assert link in self['data']['relationships'][relation_type]['links']['related']
        except AssertionError:
            self.pprint()
            raise AttributeError("Link '%s' not found in relationship '%s'" % (link, relation_type))

    def assertHasAttribute(self, attribute, value):
        """Assert a response attribute has a specific value
        """
        try:
            assert self._get_attribute(attribute) == value
        except AssertionError:
            self.pprint()
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def assertHasIncludeId(self, relationships, value):
        """Assert a response relation has a specific value
        """
        try:
            assert 'data' in self
            assert 'relationships' in self['data']
            assert relationships in self['data']['relationships']
            assert 'data' in self['data']['relationships'][relationships]
            assert self['data']['relationships'][relationships]['data'] is not None
            assert 'id' in self['data']['relationships'][relationships]['data']
            assert self['data']['relationships'][relationships]['data']['id'] == str(value)
        except AssertionError:
            self.pprint()
            raise AttributeError("Included relationships '%s' not found in response." % relationships)

    def assertHasIncludes(self, relationships, value):
        raise Unimplemented("Function assertHasIncludes is not yet implemented")

    def assertCreationDateTime(self):
        self.assertDateTimePresent('created-on-datetime')

    def assertUpdatedDateTime(self):
        self.assertDateTimePresent('updated-on-datetime')

    def assertDateTimePresent(self, attribute):
        try:
            date_time = self._get_attribute(attribute)
            assertIsDateTime(date_time)
        except AssertionError:
            self.pprint()
            raise AttributeError("Attribute '%s' was not parsed as a datetime." % attribute)

    def assertRaiseJsonApiError(self, pointer):
        """Assert an error response has a specific pointer
        """
        try:
            assert 'errors' in self
            for error in self['errors']:
                assert 'source' in error
                assert 'pointer' in error['source']
                if pointer in error['source']['pointer']:
                    return True
        except AssertionError:
            self.pprint()
            raise

    def pprint(self):
        pprint.pprint(self)
