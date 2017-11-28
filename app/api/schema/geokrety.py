from app.api.helpers.utilities import dasherize
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class GeokretSchemaPublic(Schema):

    class Meta:
        type_ = 'geokret'
        self_view = 'v1.geokret_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.geokrety_list'
        inflect = dasherize
        ordered = True

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    missing = fields.Boolean(dump_only=True)
    distance = fields.Integer(dump_only=True)
    caches_count = fields.Integer(dump_only=True)
    pictures_count = fields.Integer(dump_only=True)
    average_rating = fields.Float(dump_only=True)
    created_on_date_time = fields.Date(dump_only=True)
    updated_on_date_time = fields.Date(dump_only=True)

    owner = Relationship(
        attribute='owner',
        self_view='v1.geokret_owner',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'id': '<owner_id>'},
        schema='UserSchemaPublic',
        type_='user'
    )

    holder = Relationship(
        attribute='holder',
        self_view='v1.geokret_holder',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'id': '<holder_id>'},
        schema='UserSchemaPublic',
        type_='user'
    )


class GeokretSchema(GeokretSchemaPublic):

    class Meta:
        type_ = 'geokret'
        self_view = 'v1.geokret_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.geokrety_list'
        inflect = dasherize
        ordered = True

    tracking_code = fields.Str(dump_only=True)
