# -*- coding: utf-8 -*-

import pprint


class BasePayload(dict):

    TYPES = [
        'geokret',
        'move',
        'user',
    ]

    def __init__(self, type):
        if type not in self.TYPES:
            raise AttributeError("Invalid Payload type")

        self.update({
            "data": {
                "type": type
            }
        })
        self.blend()

    def _set_attribute(self, name, value):
        if 'attributes' not in self['data']:
            self['data']['attributes'] = {}
        if name not in self['data']['attributes']:
            self['data']['attributes'][name] = {}

        self['data']['attributes'][name] = value
        return self

    def _set_relationship(self, relationship, name, id):
        if 'relationships' not in self['data']:
            self['data']['relationships'] = {}
        if relationship not in self['data']['relationships']:
            self['data']['relationships'][relationship] = {}

        self['data']['relationships'][relationship].update({
            'data': {
                'type': name,
                'id': id,
            }
        })
        return self

    def blend(self):
        raise NotImplementedError("`blend` is not implemented")

    def set_obj(self, obj):
        raise NotImplementedError("`set_obj` is not implemented")

    def pprint(self):
        pprint.pprint(self)
