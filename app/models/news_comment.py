import datetime

from sqlalchemy import ForeignKeyConstraint, event
from sqlalchemy.ext.hybrid import hybrid_property

import bleach
import characterentities
from app.models import db
from app.views.pika_ import pika_


class NewsComment(db.Model):
    __tablename__ = 'gk-news-comments'

    id = db.Column(
        'comment_id',
        db.Integer,
        primary_key=True,
        key='id'
    )

    news_id = db.Column(
        'news_id',
        db.Integer,
        db.ForeignKey('gk-news.id'),
        key='news_id',
        nullable=False
    )

    author_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('gk-users.id', name='fk_news_comment_author'),
        key='author_id',
        nullable=False
    )

    ForeignKeyConstraint(
        ['author_id'], ['user.id'],
        use_alter=True,
        name='fk_news_comment_author'
    )

    created_on_datetime = db.Column(
        'date',
        db.DateTime,
        key='created_on_datetime',
        nullable=False,
        default=datetime.datetime.utcnow
    )

    _comment = db.Column(
        'comment',
        db.String(1000),
        nullable=False
    )

    icon = db.Column(
        db.Integer,
        default=0
    )

    # news = db.relationship('News', backref=db.backref('news_comments'))
    # author = db.relationship('User', backref=db.backref('news_comments'))

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


@event.listens_for(db.session, 'after_flush')
def after_flush(session, flush_context):
    for instance in session.new:
        if not isinstance(instance, NewsComment):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.news-comment.insert",
                                      body="news_comment_id:{0.id}".format(instance))

    for instance in session.dirty:
        if not isinstance(instance, NewsComment):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.news-comment.update",
                                      body="news_comment_id:{0.id}".format(instance))

    for instance in session.deleted:
        if not isinstance(instance, NewsComment):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.news-comment.delete",
                                      body="news_comment_id:{0.id}".format(instance))
