from app.api.helpers.data_layers import MOVE_TYPE_COMMENT
from app.api.helpers.utilities import dasherize
from app.models.move import Move
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
    tracking_code = fields.Method('tracking_code_or_none')

    def tracking_code_or_none(self, geokret):
        """Add the tracking_code only if user has already touched the GK
        """
        if not self.context['current_identity']:
            return None

        # Is GeoKret already seen?
        count = Move.query \
            .filter(Move.geokret_id == geokret.id) \
            .filter(Move.author_id == self.context['current_identity'].id) \
            .filter(Move.move_type_id != MOVE_TYPE_COMMENT) \
            .count()
        if count:
            return geokret.tracking_code


class GeokretSchema(GeokretSchemaPublic):

    class Meta:
        type_ = 'geokret'
        self_view = 'v1.geokret_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.geokrety_list'
        inflect = dasherize
        ordered = True

    tracking_code = fields.Str(dump_only=True)
