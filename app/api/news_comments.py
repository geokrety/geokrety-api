from app.api.bootstrap import api
from app.api.helpers.db import safe_query, save_to_db
from app.api.helpers.exceptions import ForbiddenException
from app.api.schema.news_comments import NewsCommentSchema
from app.models import db
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)


class NewsCommentList(ResourceList):

    def query(self, view_kwargs):
        """Filter news-comments"""
        query_ = self.session.query(NewsComment)

        if view_kwargs.get('news_id') is not None:
            safe_query(self, News, 'id', view_kwargs['news_id'], 'news_id')
            query_ = query_.join(News).filter(News.id == view_kwargs['news_id'])

        if view_kwargs.get('author_id') is not None:
            safe_query(self, User, 'id', view_kwargs['author_id'], 'author_id')
            query_ = query_.join(User).filter(User.id == view_kwargs['author_id'])

        return query_

    def before_create_object(self, data, view_kwargs):
        user = current_identity

        # Check author_id
        if not user.is_admin and not user.is_super_admin and data['author'] != user.id:
            raise ForbiddenException({'parameter': 'author'}, 'Author {} must be yourself ({})'.format(
                data['author'], user.id))

    def after_create_object(self, obj, data, view_kwargs):
        # Increment comment count on news
        news = safe_query(self, News, 'id', obj.news_id, 'id')
        news.comments_count += 1
        save_to_db(news)

    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )
    schema = NewsCommentSchema
    data_layer = {
        'session': db.session,
        'model': NewsComment,
        'methods': {
            'query': query,
            'before_create_object': before_create_object,
            'after_create_object': after_create_object
        }
    }


class NewsCommentDetail(ResourceDetail):

    def after_delete_object(self, obj, view_kwargs):
        # Decrement comment count on news
        news = safe_query(self, News, 'id', obj.news_id, 'id')
        news.comments_count -= 1
        save_to_db(news)

    decorators = (
        api.has_permission('is_user_itself', methods="PATCH,DELETE",
                           fetch="author_id", fetch_as="user_id", model=NewsComment),
    )
    schema = NewsCommentSchema
    data_layer = {
        'session': db.session,
        'model': NewsComment,
        'methods': {
            'after_delete_object': after_delete_object
        }
    }


class NewsCommentRelationship(ResourceRelationship):
    methods = ['GET']
    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment}
