from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)

from app.api.schema.badges import BadgeSchema
from app.models import db
from app.models.badge import Badge
from app.models.user import User


class BadgeList(ResourceList):
    methods = ('GET',)
    schema = BadgeSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': User,
    }


class BadgeDetail(ResourceDetail):
    methods = ('GET',)
    schema = BadgeSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Badge,
    }


class BadgeRelationship(ResourceRelationship):
    methods = ('GET',)
    schema = BadgeSchema
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Badge,
    }
