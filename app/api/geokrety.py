from app.api.bootstrap import api
from app.api.helpers.db import safe_query
from app.api.helpers.permission_manager import has_access
from app.api.schema.geokrety import GeokretSchema, GeokretSchemaPublic
from app.models import db
from app.models.geokret import Geokret
from app.models.user import User
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)


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

        return query_

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            # Is admin?
            if has_access('is_admin', user_id=current_identity.id):
                self.schema = GeokretSchema

            # List owned geokret
            if kwargs.get('owner_id') is not None and kwargs.get('owner_id') == current_identity.id:
                self.schema = GeokretSchema

            # List held geokret
            if kwargs.get('holder_id') is not None and kwargs.get('holder_id') == current_identity.id:
                self.schema = GeokretSchema

    def post(self, *args, **kwargs):
        self.schema = GeokretSchema
        return super(GeokretList, self).post(args, kwargs)

    current_identity = current_identity
    schema = GeokretSchemaPublic
    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )
    data_layer = {
        'session': db.session,
        'model': Geokret,
        'methods': {
            'query': query,
        }
    }


class GeokretDetail(ResourceDetail):

    def before_marshmallow(self, args, kwargs):
        if current_identity:
            # Is admin?
            if has_access('is_admin', user_id=current_identity.id):
                self.schema = GeokretSchema

            # Is GeoKret owner?
            if kwargs.get('id') is not None:
                geokret = safe_query(self, Geokret, 'id', kwargs['id'], 'geokret_owned_id')
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
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }


class GeokretRelationship(ResourceRelationship):
    methods = ['GET']
    schema = GeokretSchemaPublic
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }
