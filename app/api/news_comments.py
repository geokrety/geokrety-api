from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from app.models import db
from app.models.news import News
from app.models.news_comment import NewsComment
from app.api.schema.news_comments import NewsCommentSchema


class NewsCommentList(ResourceList):

    def query(self, view_kwargs):
        query_ = self.session.query(NewsComment)
        if view_kwargs.get('news_id') is not None:
            try:
                self.session.query(News).filter_by(id=view_kwargs['news_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'news_id'}, "News: {} not found".format(view_kwargs['news_id']))
            else:
                query_ = query_.join(News).filter(News.id == view_kwargs['news_id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        print("DEBUG A")
        if view_kwargs.get('news_id') is not None:
            print("DEBUG B")
            news = self.session.query(News).filter_by(id=view_kwargs['news_id']).one()
            data['news_id'] = news.id
        print("DEBUG C")

    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment,
                  'methods': {'query': query,
                              'before_create_object': before_create_object}}


class NewsCommentDetail(ResourceDetail):
    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment}


class NewsCommentRelationship(ResourceRelationship):
    schema = NewsCommentSchema
    data_layer = {'session': db.session,
                  'model': NewsComment}
