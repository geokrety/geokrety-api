import datetime

from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

import bleach
import characterentities
from app.models import db
from app.views.pika_ import pika_


class Badge(db.Model):
    __tablename__ = 'gk-badges-collection'

    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
        key='id',
    )

    _name = db.Column(
        'name',
        db.String(80),
        key='name',
        nullable=False,
        unique=True,
    )

    _description = db.Column(
        'description',
        db.String(128),
        key='description',
        nullable=True,
    )

    filename = db.Column(
        'filename',
        db.String(32),
        key='filename',
        nullable=False,
    )

    created_on_datetime = db.Column(
        'date',
        db.DateTime,
        key='created_on_datetime',
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    author_id = db.Column(
        'author_id',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='author_id',
        nullable=False,
        default=None,
    )
    author = db.relationship("User", foreign_keys=[author_id], backref="created_badges")

    @hybrid_property
    def name(self):
        return characterentities.decode(self._name)

    @name.setter
    def name(self, name):
        name_clean = bleach.clean(name, strip=True)
        self._name = characterentities.decode(name_clean).strip()

    @name.expression
    def name(cls):
        return cls._name

    @hybrid_property
    def description(self):
        if self._description is None:
            return None
        return characterentities.decode(self._description)

    @description.setter
    def description(self, description):
        description_clean = bleach.clean(description, strip=True)
        self._description = characterentities.decode(description_clean).strip()

    @description.expression
    def description(cls):
        return cls._description


@event.listens_for(db.session, 'after_flush')
def after_flush(session, flush_context):
    for instance in session.new:
        if not isinstance(instance, Badge):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.badge.insert",
                                      body=u"badge_id:{0.id}"
                                      u"name:{0.name}".format(instance))

    for instance in session.dirty:
        if not isinstance(instance, Badge):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.badge.update",
                                      body=u"badge_id:{0.id}"
                                      u"name:{0.name}".format(instance))

    for instance in session.deleted:
        if not isinstance(instance, Badge):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.badge.delete",
                                      body=u"badge_id:{0.id}"
                                      u"name:{0.name}".format(instance))
