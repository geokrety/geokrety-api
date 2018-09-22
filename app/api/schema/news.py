from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from app.api.helpers.utilities import dasherize


# Create logical data abstraction
class NewsSchema(Schema):
    class Meta:
        type_ = 'news'
        self_view = 'v1.news_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.news_list'
        inflect = dasherize
        strict = True
        ordered = True

    id = fields.Str(dump_only=True)
    # publication_date_time = fields.Date()
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    username = fields.Str()
    comments_count = fields.Integer(dump_only=True)
    created_on_datetime = fields.Date(dump_only=True)
    last_comment_date_time = fields.Date(dump_only=True)

    author = Relationship(attribute='author',
                          self_view='v1.news_author',
                          self_view_kwargs={'id': '<id>'},
                          related_view='v1.user_details',
                          related_view_kwargs={'news_author_id': '<id>'},
                          schema='UserSchemaPublic',
                          type_='user',
                          include_resource_linkage=True
                          )

    news_comments = Relationship(self_view='v1.news_comments',
                                 self_view_kwargs={'id': '<id>'},
                                 related_view='v1.news_comments_list',
                                 related_view_kwargs={'news_id': '<id>'},
                                 many=True,
                                 schema='NewsCommentSchema',
                                 type_='news-comment',
                                 #   include_resource_linkage=True
                                 )
