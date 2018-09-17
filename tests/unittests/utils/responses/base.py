# -*- coding: utf-8 -*-

import pprint


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
