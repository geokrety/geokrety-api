from app.api.helpers.exceptions import UnprocessableEntity
from app.api.helpers.utilities import dasherize
from app.models.user import User
from marshmallow import validates
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class UserSchemaPublic(Schema):

    class Meta:
        type_ = 'user'
        self_view = 'v1.user_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.users_list'
        inflect = dasherize
        ordered = True

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    language = fields.Str()
    country = fields.Str(dump_only=True)
    join_date_time = fields.Date(dump_only=True)

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

    @validates('name')
    def validate_username_uniqueness(self, data):
        if User.query.filter_by(name=data).count():
            raise UnprocessableEntity({'pointer': '/data/attributes/name'},
                                      "Username already taken")

    @validates('email')
    def validate_email_uniqueness(self, data):
        if User.query.filter_by(email=data).count():
            raise UnprocessableEntity({'pointer': '/data/attributes/email'},
                                      "Email already taken")

    class Meta:
        type_ = 'user'
        self_view = 'v1.user_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.users_list'
        inflect = dasherize
        ordered = True

    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    latitude = fields.Float()
    longitude = fields.Float()
    daily_mails = fields.Boolean()
    observation_radius = fields.Integer()
    hour = fields.Integer(dump_only=True)
    secid = fields.Str()
    statpic_id = fields.Integer()
    last_update_date_time = fields.Date(dump_only=True)
    last_mail_date_time = fields.Date(dump_only=True)
    last_login_date_time = fields.Date(dump_only=True)
