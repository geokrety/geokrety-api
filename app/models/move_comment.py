# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import event, inspect
from sqlalchemy.ext.hybrid import hybrid_property

import bleach
import characterentities
from app.api.helpers.data_layers import (MOVE_COMMENT_TYPE_MISSING,
                                         MOVE_TYPE_ARCHIVED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_SEEN, MOVE_TYPES_TEXT)
from app.api.helpers.exceptions import UnprocessableEntity
from app.models import db
from app.views.pika_ import pika_


class MoveComment(db.Model):
    __tablename__ = 'gk-ruchy-comments'

    id = db.Column(
        'comment_id',
        db.Integer,
        primary_key=True,
        key='id',
    )

    move_id = db.Column(
        'ruch_id',
        db.Integer,
        db.ForeignKey('gk-ruchy.id'),
        key='move_id',
        nullable=False,
    )

    move = db.relationship(
        "Move",
        foreign_keys=[move_id],
        backref="comments",
    )

    author_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('gk-users.id', name='fk_move_comment_author'),
        key='author_id',
        nullable=False,
    )

    author = db.relationship(
        "User",
        foreign_keys=[author_id],
        backref="moves_comments",
    )

    geokret_id = db.Column(
        'kret_id',
        db.Integer,
        db.ForeignKey('gk-geokrety.id', name='fk_move_comment_geokret'),
        key='geokret_id',
        nullable=False,
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
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    _comment = db.Column(
        'comment',
        db.String(1000),
        nullable=False,
    )

    type = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    @hybrid_property
    def comment(self):
        return characterentities.decode(self._comment)

    @comment.setter
    def comment(self, comment):
        # Drop all html tags
        comment_clean = bleach.clean(comment, strip=True)
        # Strip spaces
        self._comment = characterentities.decode(comment_clean).strip()

    @comment.expression
    def comment(cls):
        return cls._comment

    def is_missing_authorized(self):
        if self.type != MOVE_COMMENT_TYPE_MISSING:
            return True
        if self.move.geokret.last_position is not None and \
                self.move.geokret.last_position.id != self.move.id:
            raise UnprocessableEntity("Cannot declare missing on old moves",
                                      {'pointer': '/data/relationships/move/data'})
        if self.move.type in [MOVE_TYPE_DROPPED,
                              MOVE_TYPE_SEEN,
                              MOVE_TYPE_ARCHIVED]:
            return True
        raise UnprocessableEntity("Cannot declare missing on move_type %s" %
                                  MOVE_TYPES_TEXT[self.move.type],
                                  {'pointer': '/data/relationships/move/data'})


@event.listens_for(MoveComment, 'before_insert')
def before_insert_listener(mapper, connection, target):
    target.geokret_id = target.move.geokret.id
    target.is_missing_authorized()


@event.listens_for(MoveComment, "before_update")
def before_update(mapper, connection, target):
    target.is_missing_authorized()


def _has_changes_that_need_recompute(instance):
    if inspect(instance).attrs.type.history.has_changes() or \
            inspect(instance).attrs.move.history.has_changes():
        return True


@event.listens_for(db.session, 'after_flush')
def after_flush(session, flush_context):
    for instance in session.new:
        if not isinstance(instance, MoveComment):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokret.move-comment.insert",
                                      body="geokret_id:{0.move.geokret.id} "
                                      "move_id:{0.move.id} "
                                      "move_type:{0.move.type} "
                                      "user_id:{0.move.author.id} "
                                      "move_comment_type:{0.type}".format(instance))

    for instance in session.dirty:
        if not isinstance(instance, MoveComment):
            continue
        if _has_changes_that_need_recompute(instance):
            with pika_.pool.acquire() as cxn:
                cxn.channel.basic_publish(exchange='geokrety',
                                          routing_key="geokret.move-comment.update",
                                          body="geokret_id:{0.move.geokret.id} "
                                          "move_id:{0.move.id} "
                                          "move_type:{0.move.type} "
                                          "user_id:{0.move.author.id} "
                                          "move_comment_type:{0.type}".format(instance))
                if inspect(instance).attrs.move.history.has_changes():
                    for old_move_id in inspect(instance).attrs.move.history[2]:
                        cxn.channel.basic_publish(exchange='geokrety',
                                                  routing_key="geokret.move-comment.update",
                                                  body="geokret_id:{0.move.geokret.id} "
                                                  "move_id:{1} "
                                                  "move_type:{0.move.type} "
                                                  "user_id:{0.move.author.id} "
                                                  "move_comment_type:{0.type}".format(instance, old_move_id))

    for instance in session.deleted:
        if not isinstance(instance, MoveComment):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokret.move-comment.delete",
                                      body="geokret_id:{0.move.geokret.id} "
                                      "move_id:{0.move.id} "
                                      "move_type:{0.move.type} "
                                      "user_id:{0.move.author.id} "
                                      "move_comment_type:{0.type}".format(instance))
