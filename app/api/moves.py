from datetime import datetime, timedelta

from flask import request
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from sqlalchemy.orm.exc import NoResultFound

from app.api.bootstrap import api
from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from app.api.helpers.db import safe_query
from app.api.helpers.exceptions import ForbiddenException, UnprocessableEntity
from app.api.helpers.permission_manager import has_access
from app.api.schema.moves import (MoveArchiveSchema, MoveCommentSchema,
                                  MoveDippedSchema, MoveDroppedSchema,
                                  MoveGrabbedSchema, MoveSeenSchema,
                                  MoveWithCoordinatesSchema)
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move


def get_schema_by_move_type(move_type_id):
    if move_type_id == MOVE_TYPE_GRABBED:
        return MoveGrabbedSchema
    if move_type_id == MOVE_TYPE_COMMENT:
        return MoveCommentSchema
    if move_type_id == MOVE_TYPE_ARCHIVED:
        return MoveArchiveSchema
    if move_type_id == MOVE_TYPE_DROPPED:
        return MoveDroppedSchema
    if move_type_id == MOVE_TYPE_SEEN:
        return MoveSeenSchema
    if move_type_id == MOVE_TYPE_DIPPED:
        return MoveDippedSchema

    raise UnprocessableEntity("Move Type Id is invalid",
                              {'pointer': '/data/attributes/type'})


class MovesList(ResourceList):

    def post(self, *args, **kwargs):
        json_data = request.get_json()

        if 'data' in json_data:
            # Configure schema dynamically
            if 'relationships' in json_data['data'] and \
                    'type' in json_data['data']['relationships']:
                move_type_id = json_data['data']['relationships']['type']['data']['id']
                self.schema = get_schema_by_move_type(move_type_id)

            # Disallow override author relationship for non admin user
            if 'relationships' in json_data['data'] and \
                    'author' in json_data['data']['relationships']:
                if not current_identity or current_identity and not current_identity.is_admin:
                    raise ForbiddenException('Author Relationship override disallowed',
                                             {'pointer': '/data/relationships/author'})

        return super(MovesList, self).post(args, kwargs)

    def before_post(self, args, kwargs, data=None):
        # Don't leave tracking_code as it doesn't exists in database
        if 'tracking_code' in data:
            tracking_code = data['tracking_code']
            del data['tracking_code']

        # Get GeoKret ID from tracking_code
        self.geokret = safe_query(self, Geokret, 'tracking_code', tracking_code, 'tracking-code')
        data["geokret"] = self.geokret.id

        # Move cannot be done before GeoKret birth
        if data['moved_on_datetime'] < self.geokret.created_on_datetime:
            raise UnprocessableEntity("Move date cannot be prior GeoKret birth date",
                                      {'pointer': '/data/attributes/moved-on-datetime'})

        # Move cannot be done in the future
        if data['moved_on_datetime'] > datetime.utcnow().replace(microsecond=0) + timedelta(seconds=1):
            raise UnprocessableEntity("Move date cannot be in the future",
                                      {'pointer': '/data/attributes/moved-on-datetime'})

        # Identical move date is forbidden
        try:
            db.session.query(Move).filter(
                Move.moved_on_datetime == str(data['moved_on_datetime']),
                Move.geokret_id == str(self.geokret.id)
            ).one()
            raise UnprocessableEntity("There is already a move at that time",
                                      {'pointer': '/data/attributes/moved-on-datetime'})
        except NoResultFound:
            pass

        # Force current connected user as author
        if has_access('is_admin'):
            if "author" not in data:
                data["author"] = current_identity.id
        else:
            data["author"] = current_identity.id

        # Archived move type has special security requirements
        if data['type'] == MOVE_TYPE_ARCHIVED:
            if not has_access('is_geokret_owner', geokret_id=self.geokret.id):
                raise ForbiddenException('Must be the GeoKret Owner', {'pointer': '/data/attributes/geokret-id'})

    def after_post(self, result):
        from app.api.helpers.move_tasks import (
            update_move_country_and_altitude,
            update_move_distances,
            update_geokret_total_moves_count,
            update_geokret_holder,
        )

        # Enhance Move content
        update_move_country_and_altitude.delay(result['data']['id'])
        update_move_distances.delay(self.geokret.id)

        # Enhance GeoKret content
        update_geokret_total_moves_count.delay(self.geokret.id)
        update_geokret_holder.delay(self.geokret.id)
        db.session.commit()

        # TODO Generate static files
        # * gpx
        # * csv
        # * geojson
        # * statpic owner
        # * statpic mover
        # *

    schema = MoveWithCoordinatesSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )

    data_layer = {
        'session': db.session,
        'model': Move,
        'methods': {
            # 'before_create_object': before_create_object,
            # 'apply_relationships': apply_relationships,
        }
    }


class MoveDetail(ResourceDetail):

    def before_marshmallow(self, args, kwargs):
        # Configure schema dynamically
        if kwargs.get('id') is not None:
            move = safe_query(self, Move, 'id', kwargs['id'], 'id')
            self.schema = get_schema_by_move_type(move.type)

    current_identity = current_identity
    decorators = (
        api.has_permission('is_move_author', methods="DELETE",
                           fetch="id", fetch_as="move_id",
                           model=Move, fetch_key_url="id"),
    )
    methods = ('GET', 'DELETE')
    schema = MoveGrabbedSchema
    data_layer = {
        'session': db.session,
        'model': Move,
    }


class MoveRelationship(ResourceRelationship):
    methods = ['GET']
    schema = MoveGrabbedSchema
    data_layer = {
        'session': db.session,
        'model': Move,
    }
