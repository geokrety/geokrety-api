from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

from app.api.bootstrap import api
from app.models import db
from app.api.schema.users import UserSchema  #, UserSchemaPublic
from app.api.helpers.permission_manager import has_access
from app.api.helpers.db import safe_query

from app.models.user import User
from app.models.news import News
from app.models.news_comment import NewsComment

# from app.api.helpers.permission_manager import is_user_itself


class UserList(ResourceList):
    decorators = (api.has_permission('is_admin', methods="GET"),)
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserDetail(ResourceDetail):

    # decorators = (api.has_permission('is_user_itself', fetch="id", fetch_as="user_id",
    #                                  model=User,
    #                                  fetch_key_url="id"), )

    def before_get_object(self, view_kwargs):
        """
        before get method for user object
        :param view_kwargs:
        :return:
        """

        if view_kwargs.get('news_id') is not None:
            news = safe_query(self, News, 'id', view_kwargs['news_id'], 'news_id')
            if news.author_id is not None:
                view_kwargs['id'] = news.author_id
            else:
                view_kwargs['id'] = None

        if view_kwargs.get('newscomment_id') is not None:
            newscomment = safe_query(self, NewsComment, 'id', view_kwargs['newscomment_id'], 'newscomment_id')
            view_kwargs['id'] = newscomment.author_id

        # restrict access to personnal data
        # self.schema = UserSchemaPublic
        if (has_access('is_user_itself', user_id=view_kwargs['id'])):
            self.schema = UserSchema

    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User,
                  'methods': {
                      'before_get_object': before_get_object
                      }
                  }


class UserRelationship(ResourceRelationship):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}
