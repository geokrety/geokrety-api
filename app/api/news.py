from app.api.bootstrap import api
from app.api.helpers.db import safe_query
from app.api.schema.news import NewsSchema
from app.models import db
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)


class NewsList(ResourceList):

    def query(self, view_kwargs):
        """Filter news"""
        query_ = self.session.query(News)

        if view_kwargs.get('author_id') is not None:
            safe_query(self, User, 'id', view_kwargs['author_id'], 'author_id')
            query_ = query_.join(User).filter(User.id == view_kwargs['author_id'])

        return query_

    schema = NewsSchema
    decorators = (
        api.has_permission('is_admin', methods="POST"),
    )
    data_layer = {
        'session': db.session,
        'model': News,
        'methods': {
            'query': query
        }
    }


class NewsDetail(ResourceDetail):

    def before_get_object(self, view_kwargs):
        """
        before get method for news object
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('newscomment_id') is not None:
            newscomment = safe_query(self, NewsComment, 'id', view_kwargs['newscomment_id'], 'newscomment_id')
            view_kwargs['id'] = newscomment.news_id

    decorators = (
        api.has_permission('is_admin', methods="PATCH,DELETE",
                           fetch="author_id", fetch_as="user_id", model=News),
        # api.has_permission('is_admin', methods="PATCH,DELETE",
        #                    fetch="author_id", fetch_as="user_id", model=News),
    )
    schema = NewsSchema
    data_layer = {
        'session': db.session,
        'model': News,
        'methods': {
            'before_get_object': before_get_object
        }
    }


class NewsRelationship(ResourceRelationship):
    schema = NewsSchema
    data_layer = {'session': db.session,
                  'model': News}
