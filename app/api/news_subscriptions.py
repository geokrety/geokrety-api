from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)

from app.api.bootstrap import api
from app.api.helpers.exceptions import ForbiddenException, UnprocessableEntity
from app.api.helpers.permission_manager import has_access
from app.api.schema.news_subscriptions import NewsSubscriptionSchema
from app.models import db
from app.models.news_subscription import NewsSubscription


class NewsSubscriptionList(ResourceList):

    def query(self, view_kwargs):
        """Filter news-subscriptions"""
        query_ = self.session.query(NewsSubscription)
        user = current_identity

        if user.is_admin:
            return query_

        query_ = query_.filter(NewsSubscription.user_id == user.id)

        return query_

    def before_create_object(self, data, view_kwargs):

        # Check author_id
        if not data.get('subscribed'):
            raise UnprocessableEntity('Setting subscribed to False has no sense', {'pointer': '/data/attributes/subscribed'})

        if has_access('is_admin'):
            return

        # Set author to current user by default
        user = current_identity
        if 'user' not in data:
            data['user'] = user.id

        # Check author_id
        if data['user'] != user.id:
            raise ForbiddenException({'parameter': 'user'}, 'User {} must be yourself ({})'.format(
                data['user'], user.id))

    def after_create_object(self, obj, data, view_kwargs):
        # Delete row if subscribe is false
        if not obj.subscribed:
            self.session.query(NewsSubscription).filter(
                NewsSubscription.user_id == obj.user_id,
                NewsSubscription.news_id == obj.news_id
            ).delete()

    decorators = (
        api.has_permission('auth_required', methods="GET,POST"),
    )
    methods = ['GET', 'POST']
    schema = NewsSubscriptionSchema
    data_layer = {
        'session': db.session,
        'model': NewsSubscription,
        'methods': {
            'query': query,
            'before_create_object': before_create_object,
            'after_create_object': after_create_object
        }
    }


class NewsSubscriptionDetail(ResourceDetail):

    decorators = (
        api.has_permission('is_user_itself', methods="GET,DELETE",
                           fetch="user_id", fetch_as="user_id", model=NewsSubscription),
    )
    methods = ['GET', 'DELETE']
    schema = NewsSubscriptionSchema
    data_layer = {
        'session': db.session,
        'model': NewsSubscription,
    }


class NewsSubscriptionRelationship(ResourceRelationship):

    decorators = (
        api.has_permission('is_user_itself', methods="GET",
                           fetch="user_id", fetch_as="user_id", model=NewsSubscription),
    )
    methods = ['GET']
    schema = NewsSubscriptionSchema
    data_layer = {'session': db.session,
                  'model': NewsSubscription}
