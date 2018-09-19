from marshmallow import validates
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

import htmlentities
# import bleach
from app.api.helpers.data_layers import GEOKRETY_TYPES_LIST, MOVE_TYPE_COMMENT
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.helpers.utilities import dasherize
from app.models.move import Move


class GeokretSchemaPublic(Schema):

    @validates('name')
    def validate_name_blank(self, data):
        data = htmlentities.decode(data).replace('\x00', '').strip()
        if not data:
            raise UnprocessableEntity("GeoKrety name cannot be blank", {'pointer': '/data/attributes/name'})

    @validates('type')
    def validate_geokrety_type_id_valid(self, data):
        if data not in GEOKRETY_TYPES_LIST:
            raise UnprocessableEntity("GeoKrety Type Id is invalid", {'pointer': '/data/relationships/type'})

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
    created_on_datetime = fields.Date(dump_only=True)
    updated_on_datetime = fields.Date(dump_only=True)

    owner = Relationship(
        attribute='owner',
        self_view='v1.geokret_owner',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'geokret_owned_id': '<id>'},
        schema='UserSchemaPublic',
        type_='user',
        include_resource_linkage=True,
    )

    holder = Relationship(
        attribute='holder',
        self_view='v1.geokret_holder',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'geokret_held_id': '<id>'},
        schema='UserSchemaPublic',
        type_='user',
        include_resource_linkage=True,
    )

    type = Relationship(
        attribute='type',
        self_view='v1.geokret_type',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.geokrety_type_details',
        related_view_kwargs={'geokret_id': '<id>'},
        schema='GeoKretyTypesSchema',
        type_='type',
        include_resource_linkage=True,
    )

    moves = Relationship(
        self_view='v1.move_geokret',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.moves_list',
        related_view_kwargs={'geokret_id': '<id>'},
        many=True,
        schema='MoveSchema',
        type_='move',
        #   include_resource_linkage=True
    )

    tracking_code = fields.Method('tracking_code_or_none')

    def tracking_code_or_none(self, geokret):
        """Add the tracking_code only if user has already touched the GK
        """
        if not self.context['current_identity']:
            return None

        # Is holder?
        if geokret.holder_id == self.context['current_identity'].id:
            return geokret.tracking_code

        # Is owner?
        if geokret.owner_id == self.context['current_identity'].id:
            return geokret.tracking_code

        # Is GeoKret already seen?
        count = Move.query \
            .filter(Move.geokret_id == geokret.id) \
            .filter(Move.author_id == self.context['current_identity'].id) \
            .filter(Move.move_type_id != MOVE_TYPE_COMMENT)

        if count.count():
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


class GeokretSchemaCreate(GeokretSchema):

    class Meta:
        type_ = 'geokret'
        self_view = 'v1.geokret_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.geokrety_list'
        inflect = dasherize
        ordered = True

    born_at_home = fields.Boolean()
