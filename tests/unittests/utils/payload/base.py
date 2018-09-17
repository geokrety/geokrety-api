# -*- coding: utf-8 -*-

import pprint


class BasePayload(dict):

    TYPES = [
        'geokret',
        'move',
        'user',
        'news',
        'news-subscription',
        'news-comment',
    ]

    def __init__(self, obj_type):
        if obj_type not in self.TYPES:  # pragma: no cover
            raise AttributeError("Invalid Payload type")

        self.update({
            "data": {
                "type": obj_type
            }
        })
        self.blend()

    def set_id(self, value):
        self['data']['id'] = str(value)
        return self

    def _set_attribute(self, name, value):
        name = name.replace('_', '-')
        if 'attributes' not in self['data']:
            self['data']['attributes'] = {}
        if name not in self['data']['attributes']:
            self['data']['attributes'][name] = {}

        self['data']['attributes'][name] = value
        return self

    def _set_relationships(self, relationships, name, obj_id):
        if 'relationships' not in self['data']:
            self['data']['relationships'] = {}
        if relationships not in self['data']['relationships']:
            self['data']['relationships'][relationships] = {}

        self['data']['relationships'][relationships].update({
            'data': {
                'type': name,
                'id': obj_id,
            }
        })
        return self

    def _set_relationships_many(self, relationships, name, ids):
        if 'relationships' not in self['data']:  # pragma: no cover
            self['data']['relationships'] = {}
        if relationships not in self['data']['relationships']:
            self['data']['relationships'][relationships] = {}

        datas = []
        for id_ in ids:
            datas.append({
                'type': name,
                'id': id_,
            })
        self['data']['relationships'][relationships]['data'] = datas
        return self

    def blend(self):  # pragma: no cover
        raise NotImplementedError("`blend` is not implemented")

    def set_obj(self, obj):  # pragma: no cover
        raise NotImplementedError("`set_obj` is not implemented")

    def pprint(self):
        pprint.pprint(self)
