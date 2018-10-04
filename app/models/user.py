import datetime
import random

import phpass
from flask import current_app as app
from flask import request
from sqlalchemy import event
from sqlalchemy.dialects.mysql import DOUBLE, INTEGER
from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db


class User(db.Model):
    __tablename__ = 'gk-users'

    id = db.Column(
        'userid',
        db.Integer,
        primary_key=True,
        key='id',
    )
    name = db.Column(
        'user',
        db.String(80),
        key='name',
        nullable=False,
        unique=True,
    )
    is_admin = db.Column(
        'is_admin',
        db.Boolean,
        key='is_admin',
        nullable=True,
        default=False,
    )
    _password = db.Column(
        'haslo2',
        db.String(120),
        key='password',
        nullable=False,
    )
    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True,
    )
    daily_mails = db.Column(
        'wysylacmaile',
        db.Boolean,
        key='daily_news',
        nullable=False,
        default=False,
    )
    ip = db.Column(
        db.String(39),
        nullable=True,
        default=None,
    )
    language = db.Column(
        'lang',
        db.String(2),
        key='language',
        nullable=False,
        default="",
    )
    latitude = db.Column(
        'lat',
        DOUBLE(precision=8, scale=5),
        key='latitude',
        nullable=True,
        default=None,
    )
    longitude = db.Column(
        'lon',
        DOUBLE(precision=8, scale=5),
        key='longitude',
        nullable=True,
        default=None,
    )
    observation_radius = db.Column(
        'promien',
        INTEGER(unsigned=True),
        key='observation_radius',
        default=0,
    )
    country = db.Column(
        db.String(3),
        nullable=True,
        default=None,
    )
    hour = db.Column(
        'godzina',
        db.Integer,
        key='hour',
    )
    statpic_id = db.Column(
        'statpic',
        db.Integer,
        key='statpic_id',
        default=1,
    )
    join_datetime = db.Column(
        'joined',
        db.DateTime,
        key='join_datetime',
        default=datetime.datetime.utcnow,
    )
    last_mail_datetime = db.Column(
        'ostatni_mail',
        db.DateTime,
        nullable=True,
        key='last_mail_datetime',
        default=None,
    )
    last_login_datetime = db.Column(
        'ostatni_login',
        db.DateTime,
        nullable=True,
        key='last_login_datetime',
        default=None,
    )
    last_update_datetime = db.Column(
        'timestamp',
        db.DateTime,
        key='last_update_datetime',
        default=datetime.datetime.utcnow,
    )
    secid = db.Column(
        db.String(128),
    )

    news = db.relationship(
        'News',
        backref="author",
        cascade="all,delete",
    )
    news_comments = db.relationship(
        'NewsComment',
        backref="author",
        cascade="all,delete",
    )
    news_subscriptions = db.relationship(
        'NewsSubscription',
        backref="user",
        cascade="all,delete",
    )
    geokrety_owned = db.relationship(
        'Geokret',
        backref="owner",
        foreign_keys="Geokret.owner_id",
        cascade="all,delete",
    )
    geokrety_held = db.relationship(
        'Geokret',
        backref="holder",
        foreign_keys="Geokret.holder_id",
        cascade="all,delete",
    )
    moves = db.relationship(
        'Move',
        backref="author",
        foreign_keys="Move.author_id",
        cascade="all,delete",
    )

    @hybrid_property
    def password(self):
        """
        Hybrid property for password
        :return:
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Setter for _password, saves hashed password, salt and reset_password string
        :param password:
        :return:
        """
        t_hasher = phpass.PasswordHash(11, False)
        self._password = t_hasher.hash_password(
            password.encode('utf-8') + app.config['PASSWORD_HASH_SALT']
        )

    @password.expression
    def password(cls):
        return cls._password


@event.listens_for(User, 'init')
def receive_init(target, args, kwargs):
    target.hour = random.randrange(0, 23)
    target.secid = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(84))  # TODO
    # target.join_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    target.ip = request.remote_addr
