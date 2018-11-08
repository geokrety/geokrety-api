# -*- coding: utf-8 -*-

from mixer.backend.flask import mixer

from app.api.helpers.data_layers import GEOKRET_TYPE_TRADITIONAL
from app.models.geokret import Geokret

from .base import BasePayload


class GeokretyPayload(BasePayload):
    def __init__(self):
        super(GeokretyPayload, self).__init__('geokret')
        self.set_geokrety_type(GEOKRET_TYPE_TRADITIONAL)

    def set_name(self, name):
        self._set_attribute('name', name)
        return self

    def set_description(self, description):
        self._set_attribute('description', description)
        return self

    def set_born_at_home(self, born_at_home=True):
        self._set_attribute('born_at_home', born_at_home)
        return self

    def set_owner(self, user):
        self._set_relationships('owner', 'user', str(user.id))
        return self

    def set_geokrety_type(self, geokrety_type):
        self._set_relationships('type', 'type', geokrety_type)
        return self

    def set_obj(self, obj):
        self.set_name(obj.name)
        self.set_description(obj.description)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend(Geokret))
            return self
