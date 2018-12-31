# -*- coding: utf-8 -*-

import unittest
from datetime import date, datetime
from functools import wraps

import phpass
from mixer.backend.flask import mixer
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import GEOKRET_TYPES_TEXT, MOVE_TYPES_TEXT
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.news_subscription import NewsSubscription
from app.models.user import User
from tests.unittests.mixins.responses_mixin import ResponsesMixin
from tests.unittests.setup_database import Setup


def mock_hash_password(obj, password):
    """Mock hash_password from phpass.PasswordHash"""
    return password


def mock_check_password(obj, password_1, password_2):
    """Mock check_password from phpass.PasswordHash"""
    return password_1 == password_2


# https://stackoverflow.com/a/22238613/944936
def json_serial(obj):  # pragma: no cover
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type %s not serializable" % type(obj))


def custom_name_geokrety_type(testcase_func, param_num, param):
    id_ = id2 = ''
    if 1 in param.args:
        id_ = unicode(param.args[1])
        id2 = '_%s' % unicode(param.args[0])
    name = GEOKRET_TYPES_TEXT.get(id_, id_)
    return u"%s_%s%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name),
        parameterized.to_safe_name(id2),
        testcase_func.__name__,
    )


def custom_name_geokrety_type_basic(testcase_func, param_num, param):
    id_ = unicode(param.args[0])
    name = GEOKRET_TYPES_TEXT.get(id_, id_)
    return u"%s_%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name),
        testcase_func.__name__,
    )


def custom_name_geokrety_move_type(testcase_func, param_num, param):
    id_ = unicode(param.args[0])
    name = MOVE_TYPES_TEXT.get(id_, id_)
    return u"%s_%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name),
        testcase_func.__name__,
    )


def custom_name_geokrety_double_move_type(testcase_func, param_num, param):
    id_1 = unicode(param.args[0])
    id_2 = unicode(param.args[1])
    name_1 = MOVE_TYPES_TEXT.get(id_1, id_1)
    name_2 = MOVE_TYPES_TEXT.get(id_2, id_2)
    return u"%s_%s_%s (%s)" % (
        testcase_func.__name__,
        parameterized.to_safe_name(name_1),
        parameterized.to_safe_name(name_2),
        testcase_func.__name__,
    )


def request_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.test_request_context():
            args[0].blend_users()
            return func(*args, **kwargs)
    return wrapper


class BaseTestCase(ResponsesMixin, unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = Setup.create_app()
        if getattr(self, "hash_password_original", None) is None:
            self.hash_password_original = phpass.PasswordHash.hash_password
        phpass.PasswordHash.hash_password = mock_hash_password
        phpass.PasswordHash.check_password = mock_check_password
        mixer.init_app(app)

    @classmethod
    def tearDownClass(self):
        phpass.PasswordHash.hash_password = self.hash_password_original

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        Setup.truncate_db()

    def blend_admin(self, *args, **kwargs):
        with mixer.ctx():
            return mixer.blend(User, is_admin=True, **kwargs)

    def blend_user(self, *args, **kwargs):
        with mixer.ctx():
            return mixer.blend(User, **kwargs)

    def blend_move(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(Move, **kwargs)
            return mixer.blend(Move, **kwargs)

    def blend_users(self, count=3, *args, **kwargs):
        self.admin = self.blend_admin(**kwargs)
        for i in range(1, count):
            setattr(self, 'user_{}'.format(i), self.blend_user(**kwargs))

    def blend_news(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(News, **kwargs)
            return mixer.blend(News, **kwargs)

    def blend_news_subscription(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(NewsSubscription, **kwargs)
            return mixer.blend(NewsSubscription, **kwargs)

    def blend_news_comment(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(NewsComment, **kwargs)
            return mixer.blend(NewsComment, **kwargs)

    def blend_geokret(self, *args, **kwargs):
        with mixer.ctx():
            if kwargs.get('count'):
                return mixer.cycle(kwargs.get('count')).blend(Geokret, **kwargs)
            return mixer.blend(Geokret, **kwargs)
