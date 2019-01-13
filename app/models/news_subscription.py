import datetime

from sqlalchemy import ForeignKeyConstraint, event
from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db
from app.views.pika_ import pika_


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


@event.listens_for(db.session, 'after_flush')
def after_flush(session, flush_context):
    for instance in session.new:
        if not isinstance(instance, NewsSubscription):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.news-subscription.insert",
                                      body="news_subscription_id:{0.id}".format(instance))

    for instance in session.deleted:
        if not isinstance(instance, NewsSubscription):
            continue
        with pika_.pool.acquire() as cxn:
            cxn.channel.basic_publish(exchange='geokrety',
                                      routing_key="geokrety.news-subscription.delete",
                                      body="news_subscription_id:{0.id}".format(instance))
