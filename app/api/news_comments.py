from app.api.bootstrap import api
from app.api.helpers.exceptions import ForbiddenException
from app.api.schema.news_comments import NewsCommentSchema
from app.models import db
from app.models.news import News
from app.models.news_comment import NewsComment
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound


class NewsCommentList(ResourceList):

    def query(self, view_kwargs):
        """Filter news-comments"""
        query_ = self.session.query(NewsComment)

        if view_kwargs.get('news_id') is not None:
            try:
                self.session.query(News).filter_by(id=view_kwargs['news_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'news_id'}, "News: {} not found".format(view_kwargs['news_id']))
            else:
                query_ = query_.join(News).filter(News.id == view_kwargs['news_id'])

        # TODO find comments from a user

        return query_

    def before_create_object(self, data, view_kwargs):
        # Set author to current user by default
        user = current_identity
        if 'author_id' not in data:
            data['author_id'] = user.id

        # Check author_id
        if not user.is_admin and not user.is_super_admin and data['author_id'] != user.id:
            raise ForbiddenException({'parameter': 'author_id'}, 'Author {} must be yourself ({})'.format(
                data['author_id'], user.id))

    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )
    schema = NewsCommentSchema
    data_layer = {
        'session': db.session,
        'model': NewsComment,
        'methods': {
            'query': query,
            'before_create_object': before_create_object
        }
    }


class NewsCommentDetail(ResourceDetail):
    decorators = (
        api.has_permission('is_user_itself', methods="PATCH,DELETE",
                           fetch="author_id", fetch_as="user_id", model=NewsComment),
    )
    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment}


class NewsCommentRelationship(ResourceRelationship):
    methods = ['GET', 'POST', 'PATCH']
    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment}
