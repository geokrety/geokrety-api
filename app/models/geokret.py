import datetime
import random

from sqlalchemy import ForeignKeyConstraint, event
from sqlalchemy.ext.hybrid import hybrid_property

import bleach
import characterentities
from app.models import db


class Geokret(db.Model):
    __tablename__ = 'gk-geokrety'

    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
        key='id',
    )
    tracking_code = db.Column(
        'nr',
        db.String(9),
        key='tracking_code',
        nullable=False,
        unique=True,
    )
    _name = db.Column(
        'nazwa',
        db.String(75),
        key='name',
        nullable=False,
    )
    _description = db.Column(
        'opis',
        db.Text(),
        key='description',
        nullable=False,
        default='',
    )
    type = db.Column(
        'typ',
        db.Enum('0', '1', '2', '3', '4'),
        key='type',
        nullable=False,
    )
    missing = db.Column(
        'missing',
        db.Boolean,
        key='missing',
        nullable=False,
        default=False,
    )
    distance = db.Column(
        'droga',
        db.Integer,
        key='distance',
        nullable=False,
        default=0,
    )
    caches_count = db.Column(
        'skrzynki',
        db.Integer,
        key='caches_count',
        nullable=False,
        default=0,
    )
    pictures_count = db.Column(
        'zdjecia',
        db.Integer,
        key='pictures_count',
        nullable=False,
        default=0,
    )
    created_on_datetime = db.Column(
        'data',
        db.DateTime,
        nullable=False,
        key='created_on_datetime',
        default=datetime.datetime.utcnow,
    )
    updated_on_datetime = db.Column(
        'timestamp',
        db.TIMESTAMP(timezone=True),
        key='updated_on_datetime',
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    owner_id = db.Column(
        'owner',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='owner_id',
    )
    holder_id = db.Column(
        'hands_of',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='holder_id',
    )
    moves = db.relationship(
        'Move',
        backref="geokret",
        foreign_keys="Move.geokret_id",
        cascade="all,delete",
    )

    last_position_id = db.Column(
        'ost_pozycja_id',
        db.Integer,
        db.ForeignKey('gk-ruchy.id', name='fk_geokret_last_position'),
        key='last_position_id',
        nullable=True,
        default=None,
    )

    ForeignKeyConstraint(
        ['last_position_id'], ['move.id'],
        use_alter=True, name='fk_geokret_last_position'
    )

    last_move_id = db.Column(
        'ost_log_id',
        db.Integer,
        db.ForeignKey('gk-ruchy.id'),
        key='last_move_id'
    )

    # avatar_id = db.Column(
    #     'avatarid',
    #     db.Integer,
    #     db.ForeignKey('gk-obrazki.id'),
    #     key='avatar_id'
    # )

    @property
    def average_rating(self):
        # TODO note should come from database
        return 0

    @hybrid_property
    def name(self):
        return characterentities.decode(self._name)

    @name.setter
    def name(self, name):
        # Drop all html tags
        name_clean = bleach.clean(name, tags=[], strip=True)
        # Strip spaces
        self._name = characterentities.decode(name_clean).strip()

    @name.expression
    def name(cls):
        return cls._name

    @hybrid_property
    def description(self):
        return characterentities.decode(self._description)

    @description.setter
    def description(self, description):
        # Drop all unallowed html tags
        description_clean = bleach.clean(description, strip=True)
        # Strip spaces
        self._description = characterentities.decode(description_clean).strip()

    @description.expression
    def description(cls):
        return cls._description


@event.listens_for(Geokret, 'init')
def receive_init(target, args, kwargs):
    target.tracking_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))  # TODO
