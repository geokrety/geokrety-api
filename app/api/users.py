from app.api.bootstrap import api
from app.api.helpers.db import safe_query
from app.api.helpers.exceptions import ForbiddenException
from app.api.helpers.permission_manager import has_access
from app.api.schema.users import UserSchema
from app.models import db
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)


class UserList(ResourceList):

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            if 'id' in kwargs and (has_access('is_user_itself', user_id=kwargs.get('id'))):
                self.schema = UserSchema

    decorators = (
        api.has_permission('is_anonymous', methods="POST"),
    )
    schema = UserSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {'session': db.session,
                  'model': User}


class UserDetail(ResourceDetail):

    def before_get_object(self, view_kwargs):
        """
        before get method for user object
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('news_id') is not None:
            news = safe_query(self, News, 'id', view_kwargs['news_id'], 'news_id')
            view_kwargs['id'] = news.author_id

        if view_kwargs.get('newscomment_id') is not None:
            newscomment = safe_query(self, NewsComment, 'id', view_kwargs['newscomment_id'], 'newscomment_id')
            view_kwargs['id'] = newscomment.author_id

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            if 'id' in kwargs and (has_access('is_user_itself', user_id=kwargs.get('id'))):
                self.schema = UserSchema

    def before_patch(self, args, kwargs, data):
        self.schema = UserSchema

    def before_delete(self, args, kwargs):
        # Restrict deleting to admin only
        if not has_access('is_admin'):
            raise ForbiddenException({'source': ''}, 'Access Forbidden')

    current_identity = current_identity
    decorators = (
        api.has_permission('is_user_itself', methods="PATCH,DELETE",
                           fetch="id", fetch_as="user_id",
                           model=User, fetch_key_url="id"),
    )
    methods = ('GET', 'PATCH', 'DELETE')
    schema = UserSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {'session': db.session,
                  'model': User,
                  'methods': {
                      'before_get_object': before_get_object,
                  }}


class UserRelationship(ResourceRelationship):
    methods = ['GET']
    schema = UserSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {'session': db.session,
                  'model': User}
