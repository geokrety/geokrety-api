import datetime

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
from flask import current_app as app
from flask import request
from flask_jwt import _jwt_required, current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from sqlalchemy.orm.exc import NoResultFound


def get_schema_by_move_type(move_type_id):
    move_type_id = move_type_id
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

    raise UnprocessableEntity({'pointer': '/data/attributes/move_type_id'},
                              "Move Type Id is invalid")


class MovesList(ResourceList):

    def post(self, *args, **kwargs):
        json_data = request.get_json()

        # Configure schema dynamically
        if 'data' in json_data and \
            'attributes' in json_data['data'] and \
                'move_type_id' in json_data['data']['attributes']:
            move_type_id = json_data['data']['attributes']['move_type_id']
            self.schema = get_schema_by_move_type(move_type_id)

        # Disallow override author relationship for non admin user
        if 'data' in json_data and \
            'relationships' in json_data['data'] and \
                'author' in json_data['data']['relationships']:
            if not current_identity or current_identity and not current_identity.is_admin:
                raise ForbiddenException({'source': '/data/relationships/author'},
                                         'Author Relationship override disallowed')

        # Disallow override author_id for non admin user
        if 'data' in json_data and \
            'attributes' in json_data['data'] and \
                'author_id' in json_data['data']['attributes']:
            if not current_identity or current_identity and not current_identity.is_admin:
                raise ForbiddenException({'source': '/data/attributes/author_id'}, 'author_id override disallowed')

        return super(MovesList, self).post(args, kwargs)

    def before_post(self, args, kwargs, data=None):
        # Don't leave tracking_code as it doesn't exists in database
        if 'tracking_code' in data:
            tracking_code = data['tracking_code']
            del data['tracking_code']

        # Get GeoKret ID from tracking_code
        geokret = safe_query(self, Geokret, 'tracking_code', tracking_code, 'tracking_code')
        data["geokret_id"] = geokret.id

        # Archived move type has special security requirements
        if data['move_type_id'] == MOVE_TYPE_ARCHIVED:
            if not current_identity:
                _jwt_required(app.config['JWT_DEFAULT_REALM'])

            if has_access('is_admin'):
                return

            if geokret.owner_id != current_identity.id:
                raise ForbiddenException({'source': ''}, 'Owner access is required')

        # Move date restrictions
        if 'moved_on_datetime' not in data:
            raise UnprocessableEntity({'pointer': '/data/attributes/moved_on_datetime'},
                                      "Move date time is mandatory")
        else:
            # Move cannot be done before GeoKret birth
            if data['moved_on_datetime'] < geokret.created_on_datetime:
                raise UnprocessableEntity({'pointer': '/data/attributes/moved_on_datetime'},
                                          "Move date cannot be prior GeoKret birth date")

            # Move cannot be done in the future
            if data['moved_on_datetime'] > datetime.datetime.utcnow():
                raise UnprocessableEntity({'pointer': '/data/attributes/moved_on_datetime'},
                                          "Move date cannot be in the future")

        # Identical move date is forbidden
        try:
            db.session.query(Move).filter(
                Move.moved_on_datetime == str(data['moved_on_datetime']),
                Move.geokret_id == str(geokret.id)
            ).one()
            raise UnprocessableEntity({'pointer': '/data/attributes/moved_on_datetime'},
                                      "There is already a move at that time")
        except NoResultFound:
            pass

        # Anonymous logs need username field
        if not current_identity:
            if 'username' not in data or not data['username']:
                raise UnprocessableEntity({'pointer': '/data/attributes/username'},
                                          "Username field missing")

        # Drop Username if authenticated
        if current_identity and 'username' in data:
            del data['username']

        # Force current connected user as author
        if current_identity:
            data["author_id"] = current_identity.id

    def after_post(self, result):
        from app.api.helpers.move_tasks import (
            update_move_country_and_altitude,
            update_move_distances,
            update_geokret_total_distance,
            update_geokret_total_moves_count,
            update_geokret_holder,
            # update_user_owner_stat,
            # update_user_mover_stat,
        )

        # Enhance Move content
        update_move_country_and_altitude.delay(result['data']['id'])
        update_move_distances.delay(result['data']['attributes']['geokret-id'])
        db.session.commit()

        # Enhance GeoKret content
        update_geokret_total_distance.delay(result['data']['attributes']['geokret-id'])
        update_geokret_total_moves_count.delay(result['data']['attributes']['geokret-id'])
        update_geokret_holder.delay(result['data']['attributes']['geokret-id'])
        db.session.commit()

        # TODO Generate static files
        # * gpx
        # * csv
        # * geojson
        # * statpic owner
        # * statpic mover
        # *

    current_identity = current_identity
    schema = MoveWithCoordinatesSchema
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
            self.schema = get_schema_by_move_type(move.move_type_id)

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
