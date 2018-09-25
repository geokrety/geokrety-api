# -*- coding: utf-8 -*-

import pprint
from datetime import datetime, timedelta


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
            raise AttributeError("Object id not found in response.")

    @property
    def created_on_datetime(self):
        return self._format_datetime(self.get_attribute('created-on-datetime'))

    @property
    def updated_on_datetime(self):
        return self._format_datetime(self.get_attribute('updated-on-datetime'))

    def _format_datetime(self, date_time):
        print date_time
        return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')

    def get_attribute(self, attribute):
        attribute = attribute.replace('_', '-')
        assert 'attributes' in self
        assert attribute in self['attributes']
        try:
            return self['attributes'][attribute]
        except AssertionError:
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def _get_relationships(self, relationships):
        assert 'relationships' in self
        assert relationships in self['relationships'], relationships
        return self['relationships'][relationships]

    def assertHasId(self, id):
        assert self.id == str(id)

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
            raise AttributeError(
                "assert '%s' in self['relationships']['%s']['links']['related']" % (link, relation_type))

    def assertHasRelationshipSelf(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        assert 'relationships' in self
        assert relation_type in self['relationships'], relation_type
        assert 'links' in self['relationships'][relation_type], relation_type
        assert 'self' in self['relationships'][relation_type]['links'], relation_type
        assert link in self['relationships'][relation_type]['links']['self'], relation_type

    def assertHasAttribute(self, attribute, value):
        """Assert a response attribute has a specific value
        """
        try:
            assert self.get_attribute(attribute) == value
        except AssertionError:
            raise AttributeError("Attribute value '%s' not the expected one (%s)." %
                                 (self.get_attribute(attribute), value))

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
            raise AttributeError("Relationships '%s' should be '%s' but was '%s'." %
                                 (relationships, value, rel['data']['id']))

    def assertHasRelationshipDatas(self, relationships, values, type):
        """Assert a response relation has specific values
        """
        rel = self._get_relationships(relationships)
        if values is None:
            assert rel['data'] is None
        print rel
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
            raise AttributeError("Included relationships '%s' not found in response, expected %s, found %s." % (
                relationships, str_values, rel['data']))

    def assertHasIncludes(self, relationships, value):
        raise Unimplemented("Function assertHasIncludes is not yet implemented")

    def assertCreationDateTime(self):
        self.assertDateTimePresent('created-on-datetime')

    def assertUpdatedDateTime(self):
        self.assertDateTimePresent('updated-on-datetime')

    def assertHasAttributeDateTime(self, attribute, date_time):
        self.assertDateTimePresent(attribute)
        if isinstance(date_time, datetime):
            date_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert self.get_attribute(attribute)[:-1] == date_time[:-1]

    def assertDateTimePresent(self, attribute):
        try:
            datetime = self.get_attribute(attribute)
            self.assertIsDateTime(datetime)
        except AssertionError:
            raise AttributeError("Attribute '%s' was not parsed as a datetime." % attribute)

    def assertIsDateTime(self, date_time):
        if isinstance(date_time, datetime):
            return

        try:
            datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            assert False, 'Date is not parsable'
            raise

    def assertRaiseJsonApiError(self, pointer):
        """Assert an error response has a specific pointer
        """
        assert 'errors' in self
        for error in self['errors']:
            assert 'source' in error
            assert 'pointer' in error['source']
            if pointer in error['source']['pointer']:
                return True

    def pprint(self):
        pprint.pprint(self)
