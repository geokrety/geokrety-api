import datetime

from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.hybrid import hybrid_property

import bleach
import characterentities
from app.models import db

# TODO add unicity constraint on geokret_id + moved_on_datetime


class Move(db.Model):
    __tablename__ = 'gk-ruchy'

    id = db.Column(
        'ruch_id',
        db.Integer,
        primary_key=True,
        key='id'
    )
    geokret_id = db.Column(
        'id',
        db.Integer,
        db.ForeignKey('gk-geokrety.id'),
        key='geokret_id',
        nullable=False,
        default=None
    )
    latitude = db.Column(
        'lat',
        DOUBLE(precision=8, scale=5),
        key='latitude',
        nullable=True,
        default=None
    )
    longitude = db.Column(
        'lon',
        DOUBLE(precision=8, scale=5),
        key='longitude',
        nullable=True,
        default=None
    )
    altitude = db.Column(
        'alt',
        db.Integer,
        key='altitude',
        nullable=False,
        default=-32768
    )
    country = db.Column(
        'country',
        db.String(3),
        key='country',
        nullable=False,
        default=''
    )
    distance = db.Column(
        'droga',
        db.Integer,
        key='distance',
        nullable=False,
        default=0
    )
    waypoint = db.Column(
        'waypoint',
        db.String(10),
        key='waypoint',
        nullable=False,
        default=''
    )
    _comment = db.Column(
        'koment',
        db.String(5120),
        key='comment',
        nullable=False,
        default=''
    )
    pictures_count = db.Column(
        'zdjecia',
        db.Integer,
        key='pictures_count',
        nullable=False,
        default=0
    )
    comments_count = db.Column(
        'komentarze',
        db.Integer,
        key='comments_count',
        nullable=False,
        default=0
    )
    type = db.Column(
        'logtype',
        db.Enum('0', '1', '2', '3', '4', '5'),
        key='type',
        nullable=False,
    )
    author_id = db.Column(
        'user',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='author_id',
        nullable=False,
        default=None,
    )
    username = db.Column(
        'username',
        db.String(20),
        key='username',
        nullable=False,
        default=''
    )
    moved_on_datetime = db.Column(
        'data',
        db.DateTime,
        key='moved_on_datetime',
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    created_on_datetime = db.Column(
        'data_dodania',
        db.DateTime,
        key='created_on_datetime',
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_on_datetime = db.Column(
        'timestamp',
        db.DateTime,
        key='updated_on_datetime',
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    _application_name = db.Column(
        'app',
        db.String(16),
        key='application_name',
        nullable=True
    )
    _application_version = db.Column(
        'app_ver',
        db.String(16),
        key='application_version',
        nullable=True
    )

    # geokret = db.relationship('Geokret',
    #     backref=db.backref('moves', lazy=True))

    @hybrid_property
    def comment(self):
        return characterentities.decode(self._comment)

    @comment.setter
    def comment(self, comment):
        comment_clean = bleach.clean(comment, strip=True)
        self._comment = characterentities.decode(comment_clean).strip()

    @comment.expression
    def comment(cls):
        return cls._comment

    @hybrid_property
    def application_version(self):
        if self._application_version is None:
            return None
        return characterentities.decode(self._application_version)

    @application_version.setter
    def application_version(self, application_version):
        if application_version is None:
            self._application_version = None
        else:
            application_version_clean = bleach.clean(application_version, tags=[], strip=True)
            self._application_version = characterentities.decode(application_version_clean).strip()

    @application_version.expression
    def application_version(cls):
        return cls._application_version

    @hybrid_property
    def application_name(self):
        if self._application_name is None:
            return None
        return characterentities.decode(self._application_name)

    @application_name.setter
    def application_name(self, application_name):
        if application_name is None:
            self._application_name = None
        else:
            application_name_clean = bleach.clean(application_name, tags=[], strip=True)
            self._application_name = characterentities.decode(application_name_clean).strip()

    @application_name.expression
    def application_name(cls):
        return cls._application_name


# TODO launch async tasks
# @event.listens_for(Move, 'init')
# def receive_init(target, args, kwargs):
#     target.tracking_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))  # TODO
#     target.created_on_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
