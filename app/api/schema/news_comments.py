from app.api.helpers.utilities import dasherize
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


# Create logical data abstraction
class NewsCommentSchema(Schema):
    class Meta:
        type_ = 'news-comment'
        self_view = 'v1.news_comment_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.news_comments_list'
        inflect = dasherize
        ordered = True

    id = fields.Str(dump_only=True)
    comment = fields.Str()
    icon = fields.Integer(dump_only=True)
    created_on_date = fields.Date(dump_only=True)

    author = Relationship(
        attribute='author',
        self_view='v1.news_comments_author',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'id': '<author_id>'},
        schema='UserSchema',
        type_='user',
        required=True
    )

    news = Relationship(
        attribute='news',
        self_view='v1.news_comments_news',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.news_details',
        related_view_kwargs={'id': '<news_id>'},
        schema='NewsSchema',
        type_='news',
        required=True
    )
