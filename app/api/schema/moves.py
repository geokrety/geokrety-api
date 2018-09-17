import re

from app.api.helpers.data_layers import MOVE_TYPES_LIST
from app.api.helpers.db import safe_query
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.helpers.utilities import dasherize
from app.models.geokret import Geokret
from flask_rest_jsonapi.exceptions import ObjectNotFound
from marshmallow import validates
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class MoveSchema(Schema):

    @validates('tracking_code')
    def validate_tracking_code_is_valid(self, data):
        try:
            safe_query(self, Geokret, 'tracking_code', data, 'tracking_code')
        except ObjectNotFound:
            raise UnprocessableEntity("Tracking Code is invalid", {'pointer': '/data/attributes/tracking_code'})

    @validates('move_type_id')
    def validate_move_type_id_valid(self, data):
        if data not in MOVE_TYPES_LIST:
            raise UnprocessableEntity("Move Type Id is invalid", {'pointer': '/data/attributes/move_type_id'})

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"

    id = fields.Integer(dump_only=True)
    geokret_id = fields.Integer(dump_only=True)
    tracking_code = fields.Str(required=True, load_only=True)
    author_id = fields.Str(load_only=True)
    comment = fields.Str()
    username = fields.Str()
    moved_on_date_time = fields.DateTime()
    application_name = fields.Str(required=True)
    application_version = fields.Str(required=True)
    move_type_id = fields.Str(required=True)
    altitude = fields.Integer(dump_only=True)
    country = fields.Str(dump_only=True)
    distance = fields.Integer(dump_only=True)
    pictures_count = fields.Integer(dump_only=True)
    comments_count = fields.Integer(dump_only=True)
    created_on_date_time = fields.DateTime(dump_only=True)
    updated_on_date_time = fields.DateTime(dump_only=True)

    author = Relationship(
        attribute='author',
        self_view='v1.move_author',
        self_view_kwargs={'id': '<id>'},
        related_view='v1.user_details',
        related_view_kwargs={'id': '<author_id>'},
        schema='UserSchemaPublic',
        type_='user'
    )

    # move_type = Relationship(
    #     attribute='move_type_id',
    #     self_view='v1.move_type',
    #     self_view_kwargs={'id': '<id>'},
    #     related_view='v1.move_type_details',
    #     related_view_kwargs={'id': '<move_type_id>'},
    #     schema='MoveTypeSchema',
    #     type_='moves-types'
    # )


class MoveWithCoordinatesSchema(MoveSchema):

    @validates('latitude')
    def validate_latitude_valid(self, data):
        pattern = re.compile("^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$")
        if data is not None and not pattern.match(str(data)):
            raise UnprocessableEntity({'pointer': '/data/attributes/latitude'},
                                      "Latitude is invalid")

    @validates('longitude')
    def validate_longitude_valid(self, data):
        pattern = re.compile("^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$")
        if data is not None and not pattern.match(str(data)):
            raise UnprocessableEntity({'pointer': '/data/attributes/longitude'},
                                      "Longitude is invalid")

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"

    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    waypoint = fields.Str()


class MoveDroppedSchema(MoveWithCoordinatesSchema):
    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"


class MoveSeenSchema(MoveWithCoordinatesSchema):

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"


class MoveDippedSchema(MoveWithCoordinatesSchema):

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"


class MoveGrabbedSchema(MoveSchema):

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        strict = True
        dateformat = "%Y-%m-%dT%H:%M:%S"


class MoveCommentSchema(MoveSchema):

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"


class MoveArchiveSchema(MoveSchema):

    class Meta:
        type_ = 'move'
        self_view = 'v1.move_details'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'v1.moves_list'
        inflect = dasherize
        ordered = True
        dateformat = "%Y-%m-%dT%H:%M:%S"
