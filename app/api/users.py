from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship


from app.api.bootstrap import api
from app.models import db
from app.models.user import User
from app.api.schema.users import UserSchema, UserSchemaPublic
from app.api.helpers.permission_manager import has_access

# from app.api.helpers.permission_manager import is_user_itself


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserDetail(ResourceDetail):

    # decorators = (api.has_permission('is_user_itself', fetch="id", fetch_as="user_id",
    #                                  model=User,
    #                                  fetch_key_url="id"), )

    def before_get(self, args, kwargs):
        self.schema = UserSchemaPublic
        if (has_access('is_user_itself', user_id=kwargs['id'])):
            self.schema = UserSchema

    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserRelationship(ResourceRelationship):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}
