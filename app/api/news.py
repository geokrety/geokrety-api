from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

from app.models import db
from app.models.news import News
from app.api.schema.news import NewsSchema


class NewsList(ResourceList):
    schema = NewsSchema
    data_layer = {'session': db.session,
                  'model': News}


class NewsDetail(ResourceDetail):

    # def before_get(self, args, kwargs):
    #     self.schema = NewsSchemaPublic

    # def after_get_object(self, data, view_kwargs):
    #     d = data.content.encode('latin1')
    #     pprint.pprint(d.decode('utf-8'))

    schema = NewsSchema
    data_layer = {'session': db.session,
                  'model': News,
                #   'methods': {'after_get_object': after_get_object}
                  }


class NewsRelationship(ResourceRelationship):
    schema = NewsSchema
    data_layer = {'session': db.session,
                  'model': News}
