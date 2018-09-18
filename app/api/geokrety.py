
from datetime import datetime

from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from flask_rest_jsonapi.exceptions import ObjectNotFound

from app.api.bootstrap import api
from app.api.helpers.data_layers import GEOKRETY_TYPES_LIST, MOVE_TYPE_DIPPED
from app.api.helpers.db import safe_query
from app.api.helpers.permission_manager import has_access
from app.api.schema.geokrety import (GeokretSchema, GeokretSchemaCreate,
                                     GeokretSchemaPublic)
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move
from app.models.user import User


class GeokretList(ResourceList):

    def query(self, view_kwargs):
        """Filter geokrety"""
        query_ = self.session.query(Geokret)

        # /users/<int:owner_id>/geokrety-owned
        if view_kwargs.get('owner_id') is not None:
            safe_query(self, User, 'id', view_kwargs['owner_id'], 'owner_id')
            query_ = query_.filter_by(owner_id=view_kwargs['owner_id'])

        # /users/<int:holder_id>/geokrety-held
        if view_kwargs.get('holder_id') is not None:
            safe_query(self, User, 'id', view_kwargs['holder_id'], 'holder_id')
            query_ = query_.filter_by(holder_id=view_kwargs['holder_id'])

        # /geokrety-types/<int:geokrety_type_id>/geokrety
        if view_kwargs.get('geokrety_type_id') is not None:
            if str(view_kwargs['geokrety_type_id']) not in GEOKRETY_TYPES_LIST:
                raise ObjectNotFound({'parameter': '{}'.format('geokrety_type_id')},
                                     "{}: {} not found".format('geokrety_type', view_kwargs['geokrety_type_id']))
            query_ = query_.filter_by(type=str(view_kwargs['geokrety_type_id']))

        return query_

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            # Is admin?
            if has_access('is_admin', user_id=current_identity.id):
                self.schema = GeokretSchema

            # List owned GeoKret
            if kwargs.get('owner_id') is not None and kwargs.get('owner_id') == current_identity.id:
                self.schema = GeokretSchema

            # List held GeoKret
            if kwargs.get('holder_id') is not None and kwargs.get('holder_id') == current_identity.id:
                self.schema = GeokretSchema

    def post(self, *args, **kwargs):
        self.schema = GeokretSchemaCreate
        return super(GeokretList, self).post(args, kwargs)

    def before_post(self, args, kwargs, data=None):

        # Enforce owner to current user
        if not current_identity.is_admin or 'owner' not in data:
            data['owner'] = current_identity.id

        # Enforce holder to owner
        data['holder'] = data['owner']

        if 'born_at_home' in data and data['born_at_home']:
            self.create_first_move = True
            del data['born_at_home']
        else:
            self.create_first_move = False

    def create_object(self, data, kwargs):
        geokret = self._data_layer.create_object(data, kwargs)

        # Create first move if requested
        if self.create_first_move:
            # But only if user has home coordinates
            owner = safe_query(self, User, 'id', geokret.owner_id, 'id')
            if owner.latitude and owner.longitude:
                move = Move(
                    author_id=geokret.owner_id,
                    geokret_id=geokret.id,
                    move_type_id=MOVE_TYPE_DIPPED,
                    moved_on_datetime=datetime.utcnow(),
                    latitude=owner.latitude,
                    longitude=owner.longitude,
                    comment="Born here",
                )
                db.session.add(move)
                db.session.commit()
        return geokret

    current_identity = current_identity
    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )
    data_layer = {
        'session': db.session,
        'model': Geokret,
        'methods': {
            'query': query,
        },
    }


class GeokretDetail(ResourceDetail):

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            # Is admin?
            if has_access('is_admin', user_id=current_identity.id):
                self.schema = GeokretSchema

            if kwargs.get('id') is not None:
                geokret = safe_query(self, Geokret, 'id', kwargs['id'], 'id')

                # Is GeoKret owner?
                if geokret.owner_id == current_identity.id:
                    self.schema = GeokretSchema

    current_identity = current_identity
    decorators = (
        api.has_permission('is_owner', methods="PATCH,DELETE",
                           fetch="id", fetch_as="geokret_id",
                           model=Geokret, fetch_key_url="id"),
    )
    methods = ('GET', 'PATCH', 'DELETE')
    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }


class GeokretRelationship(ResourceRelationship):
    methods = ['GET']
    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }
