import datetime
import random

import phpass
from app.models import db
from flask import current_app as app
from flask import request
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'gk-users'

    id = db.Column(
        'userid',
        db.Integer,
        primary_key=True,
        key='id'
    )
    name = db.Column(
        'user',
        db.String(80),
        key='name',
        nullable=False,
        unique=True
    )
    _password = db.Column(
        'haslo2',
        db.String(120),
        key='password',
        nullable=False
    )
    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )
    daily_mails = db.Column(
        'wysylacmaile',
        db.Boolean,
        key='daily_news',
        nullable=False,
        default=True
    )
    ip = db.Column(
        db.String(39)
    )
    language = db.Column(
        'lang',
        db.String(2),
        key='language',
        nullable=False,
        default=""
    )
    latitude = db.Column(
        'lat',
        db.Float,
        key='latitude',
        default=48.8566
    )
    longitude = db.Column(
        'lon',
        db.Float,
        key='longitude',
        default=2.3522
    )
    observation_radius = db.Column(
        'promien',
        db.Integer,
        key='observation_radius',
        default=0
    )
    country = db.Column(
        db.String(3)
    )
    hour = db.Column(
        'godzina',
        db.Integer,
        key='hour'
    )
    statpic_id = db.Column(
        'statpic',
        db.Integer,
        key='statpic_id',
        default=1
    )
    join_date_time = db.Column(
        'joined',
        db.DateTime, key='join_date_time'
    )
    last_mail_date_time = db.Column(
        'ostatni_mail',
        db.DateTime,
        nullable=True,
        key='last_mail_date_time'
    )
    last_login_date_time = db.Column(
        'ostatni_login',
        db.DateTime,
        nullable=False,
        key='last_login_date_time',
        default=datetime.datetime.utcnow
    )
    last_update_date_time = db.Column(
        'timestamp',
        db.DateTime,
        key='last_update_date_time',
        default=datetime.datetime.utcnow
    )
    secid = db.Column(
        db.String(128)
    )

    news = db.relationship(
        'News',
        backref="author",
        cascade="all,delete"
    )
    news_comments = db.relationship(
        'NewsComment',
        backref="author",
        cascade="all,delete"
    )
    news_subscriptions = db.relationship(
        'NewsSubscription',
        backref="user",
        cascade="all,delete"
    )
    geokrety_owned = db.relationship(
        'Geokret',
        backref="owner",
        foreign_keys="Geokret.owner_id",
        cascade="all,delete"
    )
    geokrety_held = db.relationship(
        'Geokret',
        backref="holder",
        foreign_keys="Geokret.holder_id",
        cascade="all,delete"
    )
    geokrety_moves = db.relationship(
        'Move',
        backref="author",
        foreign_keys="Move.author_id",
        cascade="all,delete"
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

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    @property
    def is_super_admin(self):
        return self.id in [1, 26422]

    @property
    def is_admin(self):
        return self.id in [1, 26422]


@event.listens_for(User, 'init')
def receive_init(target, args, kwargs):
    target.hour = random.randrange(0, 23)
    target.secid = "todo"  # TODO
    target.join_date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    target.ip = request.remote_addr
    target.country = 'fr'  # TODO
