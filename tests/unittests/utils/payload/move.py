# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

from mixer.backend.flask import mixer

from app.api.helpers.data_layers import MOVE_TYPES_LIST
from app.models.move import Move
from app.models.user import User
from base import BasePayload


class MovePayload(BasePayload):
    def __init__(self, move_type):
        super(MovePayload, self).__init__('move')
        self.set_move_type(move_type)
        self.move_date_time()
        self.application_name()
        self.application_version()

    def set_move_type(self, type):
        if type not in MOVE_TYPES_LIST:
            raise TypeError("'type' parameter must be a valid move type (%s)" % type)

        self._set_attribute('move_type_id', type)
        return self

    def set_coordinates(self, latitude=43.78, longitude=7.06):
        self._set_attribute('latitude', latitude)
        self._set_attribute('longitude', longitude)
        return self

    def set_tracking_code(self, tracking_code="ABC123"):
        self._set_attribute('tracking_code', tracking_code)
        return self

    def set_application_name(self, application_name="GeoKrety API"):
        self._set_attribute('application_name', application_name)
        return self

    def set_application_version(self, application_version="Unit Tests 1.0"):
        self._set_attribute('application_version', application_version)
        return self

    def set_comment(self, comment="Born here ;)"):
        self._set_attribute('comment', comment)
        return self

    def set_username(self, username="Anyone"):
        self._set_attribute('username', username)
        return self

    def set_author(self, user):
        if type(user) is not User:
            raise TypeError("'user' parameter must be of type User (%s)" % type(user))

        self._set_relationship('author', 'user', user.id)
        return self

    def set_moved_date_time(self, date_time=None):
        def random_date(start):
            """Generate a random datetime between `start` and `end`"""
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.utcnow()
            return (start + timedelta(
                # Get a random amount of seconds between `start` and `end`
                seconds=random.randint(0, int((end - start).total_seconds())),
            )).strftime("%Y-%m-%dT%H:%M:%S")

        if date_time:
            self._set_attribute('moved_on_date_time', date_time)
        else:
            self._set_attribute('moved_on_date_time', random_date("2017-12-01T14:18:22"))
        return self

    def set_obj(self, obj):
        self.set_move_type(obj.move_type)
        self.set_coordinates(obj.coordinates)
        self.set_tracking_code(obj.tracking_code)
        self.set_application_name(obj.application_name)
        self.set_application_version(obj.application_version)
        self.set_comment(obj.comment)
        self.set_username(obj.username)
        self.set_moved_date_time(obj.moved_date_time)
        if obj.author:
            self.set_author(obj.author)
        return self

    def blend(self):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend(Move))
            return self
