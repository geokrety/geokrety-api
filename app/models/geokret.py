import datetime
import random

from app.models import db
from sqlalchemy import event


class Geokret(db.Model):
    __tablename__ = 'gk-geokrety'

    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
        key='id'
    )
    tracking_code = db.Column(
        'nr',
        db.String(9),
        key='tracking_code',
        nullable=False,
        unique=True
    )
    name = db.Column(
        'nazwa',
        db.String(75),
        key='name',
        nullable=False
    )
    description = db.Column(
        'opis',
        db.Text(),
        key='description',
        nullable=False,
        default=''
    )
    type = db.Column(
        'type',
        db.Enum('0', '1', '2', '3', '4'),
        key='type'
    )
    missing = db.Column(
        'missing',
        db.Boolean,
        key='missing',
        nullable=False,
        default=False
    )
    distance = db.Column(
        'droga',
        db.Integer,
        key='distance',
        nullable=False,
        default=0
    )
    caches_count = db.Column(
        'skrzynki',
        db.Integer,
        key='caches_count',
        nullable=False,
        default=0
    )
    pictures_count = db.Column(
        'zdjecia',
        db.Integer,
        key='pictures_count',
        nullable=False,
        default=0
    )
    created_on_date_time = db.Column(
        'data',
        db.DateTime,
        nullable=False,
        key='created_on_date_time',
        default=datetime.datetime.utcnow
    )
    updated_on_date_time = db.Column(
        'timestamp',
        db.TIMESTAMP(timezone=True),
        key='updated_on_date_time',
        default=datetime.datetime.utcnow
    )
    owner_id = db.Column(
        'owner',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='owner_id'
    )
    hands_of_id = db.Column(
        'hands_of',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='hands_of_id'
    )
    # last_position_id = db.Column(
    #     'ost_pozycja_id',
    #     db.Integer,
    #     db.ForeignKey('gk-ruchy.id'),
    #     key='last_position_id'
    # )
    # last_log_id = db.Column(
    #     'ost_log_id',
    #     db.Integer,
    #     db.ForeignKey('gk-ruchy.id'),
    #     key='last_log_id'
    # )
    # avatar_id = db.Column(
    #     'avatarid',
    #     db.Integer,
    #     db.ForeignKey('gk-obrazki.id'),
    #     key='avatar_id'
    # )

    # news = db.relationship(
    #     'News',
    #     backref="author",
    #     cascade="all,delete"
    # )
    # news_comments = db.relationship(
    #     'NewsComment',
    #     backref="author",
    #     cascade="all,delete"
    # )
    # news_subscriptions = db.relationship(
    #     'NewsSubscription',
    #     backref="user",
    #     cascade="all,delete"
    # )

    def get_id(self):
        return self.id

    @property
    def average_rating(self):
        # TODO note should come from database
        return 0


@event.listens_for(Geokret, 'init')
def receive_init(target, args, kwargs):
    target.tracking_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))  # TODO
    target.created_on_date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
