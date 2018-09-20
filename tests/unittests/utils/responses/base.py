# -*- coding: utf-8 -*-

import pprint

from tests.unittests.utils import assertIsDateTime


class BaseResponse(dict):

    def __init__(self, data):
        if 'data' in data:
            self.update(data['data'])
        else:
            self.update(data)

    @property
    def id(self):
        assert 'id' in self
        try:
            return self['id']
        except AssertionError:
            self.pprint()
            raise AttributeError("Object id not found in response.")

    def get_attribute(self, attribute):
        assert 'attributes' in self
        assert attribute in self['attributes']
        try:
            return self['attributes'][attribute]
        except AssertionError:
            self.pprint()
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def _get_relationships(self, relationships):
        assert 'relationships' in self
        assert relationships in self['relationships']
        return self['relationships'][relationships]

    def assertHasRelationshipRelated(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        assert 'relationships' in self
        assert relation_type in self['relationships']
        assert 'links' in self['relationships'][relation_type]
        assert 'related' in self['relationships'][relation_type]['links']
        try:
            assert link in self['relationships'][relation_type]['links']['related']
        except AssertionError:
            self.pprint()
            raise AttributeError("assert '%s' in self['relationships']['%s']['links']['related']" % (link, relation_type))

    def assertHasRelationshipSelf(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        assert 'relationships' in self
        assert relation_type in self['relationships']
        assert 'links' in self['relationships'][relation_type]
        assert 'self' in self['relationships'][relation_type]['links']
        try:
            assert link in self['relationships'][relation_type]['links']['self']
        except AssertionError:
            print link
            self.pprint()
            raise AttributeError("assert %s in self['relationships']['%s']['links']['self']" % (link, relation_type))

    def assertHasAttribute(self, attribute, value):
        """Assert a response attribute has a specific value
        """
        try:
            assert self.get_attribute(attribute) == value
        except AssertionError:
            self.pprint()
            raise AttributeError("Attribute value '%s' not the expected one (%s)." % (self.get_attribute(attribute), value))

    def assertHasRelationshipData(self, relationships, value, type):
        """Assert a response relation has a specific value
        """
        rel = self._get_relationships(relationships)
        if value is None:
            assert rel['data'] is None
        assert rel['data'] is not None
        try:
            assert 'id' in rel['data']
            assert rel['data']['id'] == str(value)
            assert 'type' in rel['data']
            assert rel['data']['type'] == type
        except AssertionError:
            self.pprint()
            raise AttributeError("Relationships '%s' should be '%s' but was '%s'." % (rel, value, rel['data']))

    def assertHasRelationshipDatas(self, relationships, values, type):
        """Assert a response relation has specific values
        """
        rel = self._get_relationships(relationships)
        if values is None:
            assert rel['data'] is None
        assert rel['data'] is not None

        str_values = [str(value) for value in values]
        found_ids = []
        try:
            # returned data in expected list
            for data in rel['data']:
                assert 'id' in data
                assert data['id'] in str_values
                assert 'type' in data
                assert data['type'] == type
                found_ids.append(data['id'])
            # expect to find all expected values in response
            for value in str_values:
                assert value in found_ids
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
            date_time = self.get_attribute(attribute)
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
