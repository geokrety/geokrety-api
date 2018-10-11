# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

from mixer.backend.flask import mixer

from app.models.move import Move
from base import BasePayload


def random_date(start):
    """Generate a random datetime between `start` and `end`"""
    end = datetime.utcnow()
    return (start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )).strftime("%Y-%m-%dT%H:%M:%S")


class MovePayload(BasePayload):
    def __init__(self, move_type, geokret=None, moved_on_datetime=None):
        self.update({
            "data": {
                "type": 'move'
            }
        })
        self.blend(type=move_type)
        if geokret is not None:
            self.set_tracking_code(geokret.tracking_code)
            self.set_moved_on_datetime(random_date(geokret.created_on_datetime))
        if moved_on_datetime is not None:
            self.set_moved_on_datetime(moved_on_datetime)

    def set_type(self, move_type):
        self._set_relationships('type', 'move-type', move_type)
        return self

    def set_coordinates(self, latitude=43.78, longitude=7.06):
        self._set_attribute('latitude', latitude)
        self._set_attribute('longitude', longitude)
        return self

    def set_waypoint(self, waypoint):
        self._set_attribute('waypoint', waypoint)
        return self

    def set_tracking_code(self, tracking_code):
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

    def set_author(self, user_id):
        self._set_relationships('author', 'user', user_id)
        return self

    def set_moved_on_datetime(self, move_datetime=None):
        if isinstance(move_datetime, datetime):
            self._set_attribute('moved_on_datetime', move_datetime.strftime("%Y-%m-%dT%H:%M:%S"))
        else:
            self._set_attribute('moved_on_datetime', move_datetime)
        return self

    def set_obj(self, obj):
        self.set_type(obj.type)
        self.set_coordinates(obj.latitude, obj.longitude)
        self.set_application_name(obj.application_name)
        self.set_application_version(obj.application_version)
        self.set_comment(obj.comment)
        self.set_username(obj.username)
        self.set_moved_on_datetime(obj.moved_on_datetime)
        return self

    def blend(self, *args, **kwargs):
        with mixer.ctx(commit=False):
            self.set_obj(mixer.blend(Move, *args, **kwargs))
            return self
