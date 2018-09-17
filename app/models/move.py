import datetime

from app.models import db
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.hybrid import hybrid_property
import htmlentities

# TODO add unicity constraint on geokret_id + moved_on_date_time


class Move(db.Model):
    __tablename__ = 'gk-ruchy'

    @hybrid_property
    def comment(self):
        return htmlentities.decode(self._comment)

    @comment.setter
    def comment(self, comment):
        self._comment = htmlentities.encode(comment)

    @comment.expression
    def comment(cls):
        return cls._comment

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
        key='_comment',
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
    move_type_id = db.Column(
        'logtype',
        db.Enum('0', '1', '2', '3', '4', '5', '6'),
        key='move_type',
        nullable=False,
    )
    author_id = db.Column(
        'user',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='author_id',
        nullable=True,
        default=None
    )
    username = db.Column(
        'username',
        db.String(20),
        key='username',
        nullable=False,
        default=''
    )
    moved_on_date_time = db.Column(
        'data',
        db.DateTime,
        key='moved_on_date_time',
        nullable=False,
    )
    created_on_date_time = db.Column(
        'data_dodania',
        db.DateTime,
        key='created_on_date_time',
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_on_date_time = db.Column(
        'timestamp',
        db.DateTime,
        key='updated_on_date_time',
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    application_name = db.Column(
        'app',
        db.String(16),
        key='application_name',
        nullable=True
    )
    application_version = db.Column(
        'app_ver',
        db.String(16),
        key='application_version',
        nullable=True
    )

    # geokret = db.relationship('Geokret',
    #     backref=db.backref('moves', lazy=True))
