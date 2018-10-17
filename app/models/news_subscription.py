import datetime

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db


class NewsSubscription(db.Model):
    __tablename__ = 'gk-news-comments-access'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    news_id = db.Column(
        db.Integer,
        db.ForeignKey('gk-news.id'),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('gk-users.id', name='fk_news_comment_subscription'),
        nullable=False,
    )

    ForeignKeyConstraint(
        ['author_id'], ['user.id'],
        use_alter=True,
        name='fk_news_comment_subscription'
    )

    subscribed_on_datetime = db.Column(
        'read',
        db.DateTime,
        key='subscribed_on_datetime',
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    post = db.Column(
        db.Date,
        nullable=True,
    )

    _subscribed = db.Column(
        'subscribed',
        db.Integer,
        key='subscribed',
        default=1,
    )

    @hybrid_property
    def subscribed(self):
        """
        Hybrid property for subscribed
        :return:
        """
        return bool(self._subscribed)

    @subscribed.setter
    def subscribed(self, subscribed):
        """
        Setter for _subscribed, convert integer to boolean
        :param subscribed:
        :return:
        """
        self._subscribed = bool(subscribed)
