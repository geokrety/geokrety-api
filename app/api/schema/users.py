from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from app.api.helpers.utilities import dasherize


class UserSchemaPublic(Schema):

    class Meta:
        type_ = 'user'
        self_view = 'v1.user_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.users_list'
        inflect = dasherize
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.Str()
    email = fields.Str(load_only=True)
    password = fields.Str(load_only=True)
    language = fields.Str()
    country = fields.Str()

    join_date_time = fields.Date(dump_only=True)
    statpic_id = fields.Integer()

    # statpic = Relationship()
    news = Relationship(self_view='v1.user_news',
                        self_view_kwargs={'id': '<id>'},
                        related_view='v1.news_list',
                        related_view_kwargs={'author_id': '<id>'},
                        many=True,
                        schema='NewsSchema',
                        type_='news')

    news_comments = Relationship(self_view='v1.user_news_comments',
                            self_view_kwargs={'id': '<id>'},
                            related_view='v1.news_comments_list',
                            related_view_kwargs={'author_id': '<id>'},
                            many=True,
                            schema='NewsCommentSchema',
                            type_='news-comment',
                            # include_resource_linkage=True
                            )

class UserSchema(UserSchemaPublic):

    # class Meta(UserSchemaPublic.Meta):
    #     pass

    class Meta:
        type_ = 'user'
        self_view = 'v1.user_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.users_list'
        inflect = dasherize
        ordered = True

    email = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    daily_mails = fields.Boolean()
    observation_radius = fields.Integer()
    hour = fields.Integer()
    secid = fields.Str()
    last_update_date_time = fields.Date()
    last_mail_date_time = fields.Date()
    last_login_date_time = fields.Date()
