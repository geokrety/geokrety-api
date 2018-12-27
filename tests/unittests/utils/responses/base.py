# -*- coding: utf-8 -*-

import pprint
from datetime import datetime


class BaseResponse(dict):

    class assertRaises:

        def __init__(self, expected, expected_regexp=None):
            self.expected = expected
            self.failureException = AssertionError
            self.expected_regexp = expected_regexp

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, tb):  # pragma: no cover
            if exc_type is None:
                try:
                    exc_name = self.expected.__name__
                except AttributeError:
                    exc_name = str(self.expected)
                raise self.failureException(
                    "{0} not raised".format(exc_name))
            if not issubclass(exc_type, self.expected):
                # let unexpected exceptions pass through
                return False
            self.exception = exc_value  # store for later retrieval
            if self.expected_regexp is None:
                return True

            expected_regexp = self.expected_regexp
            if not expected_regexp.search(str(exc_value)):
                raise self.failureException('"%s" does not match "%s"' %
                                            (expected_regexp.pattern, str(exc_value)))
            return True

    def __init__(self, data):
        if data is None:
            self.update({})
        elif data.get('data'):
            self.update(data['data'])
        else:
            self.update(data)

    @property
    def id(self):
        assert 'id' in self
        try:
            return self['id']
        except AssertionError:  # pragma: no cover
            raise AttributeError("Object id not found in response.")

    @property
    def created_on_datetime(self):
        return self._format_datetime(self.get_attribute('created-on-datetime'))

    @property
    def updated_on_datetime(self):
        return self._format_datetime(self.get_attribute('updated-on-datetime'))

    def _format_datetime(self, date_time):
        return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')

    def get_attribute(self, attribute):
        attribute = attribute.replace('_', '-')
        assert 'attributes' in self
        assert attribute in self['attributes'], attribute
        try:
            return self['attributes'][attribute]
        except AssertionError:  # pragma: no cover
            raise AttributeError("Attribute '%s' not found in response." % attribute)

    def _get_relationships(self, relationships):
        relationships = relationships.replace('_', '-')
        assert 'relationships' in self
        assert relationships in self['relationships'], relationships
        return self['relationships'][relationships]

    def assertHasId(self, obj_id):
        assert self.id == str(obj_id)

    def assertHasRelationshipRelated(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        relation_type = relation_type.replace('_', '-')
        assert 'relationships' in self
        assert relation_type in self['relationships']
        assert 'links' in self['relationships'][relation_type]
        assert 'related' in self['relationships'][relation_type]['links']
        try:
            assert link in self['relationships'][relation_type]['links']['related']
        except AssertionError:  # pragma: no cover
            raise AttributeError(
                "assert '%s' in self['relationships']['%s']['links']['related']" % (link, relation_type))

    def assertHasRelationshipSelf(self, relation_type, link):
        """Assert an error response has a specific pointer
        """
        relation_type = relation_type.replace('_', '-')
        assert 'relationships' in self
        assert relation_type in self['relationships'], relation_type
        assert 'links' in self['relationships'][relation_type], relation_type
        assert 'self' in self['relationships'][relation_type]['links'], relation_type
        assert link in self['relationships'][relation_type]['links']['self'], link

    def assertHasAttribute(self, attribute, value):
        """Assert a response attribute has a specific value
        """
        try:
            assert self.get_attribute(attribute) == value
        except AssertionError:  # pragma: no cover
            raise AttributeError("Attribute '%s' value '%s' not the expected one (%s)." %
                                 (attribute, self.get_attribute(attribute), value))

    def assertHasRelationshipData(self, relationships, value, obj_type):
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
            assert rel['data']['type'] == obj_type
        except AssertionError:  # pragma: no cover
            raise AttributeError("Relationships '%s' should be '%s' but was '%s'." %
                                 (relationships, obj_type, rel['data']['type']))

    def assertHasRelationshipDatas(self, relationships, values, obj_type):
        """Assert a response relation has specific values
        """
        rel = self._get_relationships(relationships)
        if values is None:  # pragma: no cover
            assert rel['data'] is None, rel
        assert rel['data'] is not None, rel

        str_values = [str(value.id) for value in values]
        found_ids = []
        try:
            # returned data in expected list
            for data in rel['data']:
                assert 'id' in data
                assert data['id'] in str_values, data['id']
                assert 'type' in data
                assert data['type'] == obj_type
                found_ids.append(data['id'])
            # expect to find all expected values in response
            for value in str_values:
                assert value in found_ids
        except AssertionError:  # pragma: no cover
            raise AttributeError("Included relationships '%s' not found in response, expected %s, found %s." % (
                relationships, str_values, rel['data']))

    def assertHasIncludes(self, relationships, value):  # pragma: no cover
        raise NotImplementedError("Function assertHasIncludes is not yet implemented")

    def assertCreationDateTime(self):
        self.assertDateTimePresent('created-on-datetime')

    def assertUpdatedDateTime(self):
        self.assertDateTimePresent('updated-on-datetime')

    def assertHasAttributeDateTimeOrNone(self, attribute, date_time):
        if date_time is None:
            return
        self.assertHasAttributeDateTime(attribute, date_time)

    def assertHasAttributeDateTime(self, attribute, date_time):
        self.assertDateTimePresent(attribute)
        if isinstance(date_time, datetime):
            date_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert self.get_attribute(attribute)[:-1] == date_time[:-1]

    def assertDateTimePresent(self, attribute):
        datetime = self.get_attribute(attribute)
        self.assertIsDateTime(datetime)

    def assertIsDateTime(self, date_time):
        if isinstance(date_time, datetime):
            return

        try:
            datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:  # pragma: no cover
            assert False, 'Date is not parsable'

    def assertRaiseJsonApiError(self, pointer):
        """Assert an error response has a specific pointer
        """
        assert 'errors' in self
        for error in self['errors']:
            assert 'source' in error
            assert 'pointer' in error['source']
            if pointer in error['source']['pointer']:
                return True
        assert False, "JsonApiError pointer '{}' not raised".format(pointer)  # pragma: no cover

    def pprint(self):
        pprint.pprint(self)
