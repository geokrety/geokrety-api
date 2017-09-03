from flask_jwt import current_identity
from sqlalchemy.orm.exc import NoResultFound
from flask import request

from app.api.helpers.errors import ForbiddenError, NotFoundError
from app.api.helpers.permissions import jwt_required


@jwt_required
def auth_required(view, view_args, view_kwargs, *args, **kwargs):
    return view(*view_args, **view_kwargs)


@jwt_required
def is_super_admin(view, view_args, view_kwargs, *args, **kwargs):
    """
    Permission function for things allowed exclusively to super admin.
    Do not use this if the resource is also accessible by a normal admin, use the is_admin decorator instead.
    :return:
    """
    user = current_identity
    if not user.is_super_admin:
        return ForbiddenError({'source': ''}, 'Super admin access is required').respond()
    return view(*view_args, **view_kwargs)


@jwt_required
def is_admin(view, view_args, view_kwargs, *args, **kwargs):
    user = current_identity
    if not user.is_admin and not user.is_super_admin:
        return ForbiddenError({'source': ''}, 'Admin access is required').respond()

    return view(*view_args, **view_kwargs)


@jwt_required
def is_user_itself(view, view_args, view_kwargs, *args, **kwargs):
    """
    Allows admin and super admin access to any resource irrespective of id.
    Otherwise the user can only access his/her resource.
    """
    user = current_identity
    if not user.is_admin and not user.is_super_admin and user.id != kwargs['user_id']:
        return ForbiddenError({'source': ''}, 'Access Forbidden').respond()
    return view(*view_args, **view_kwargs)


permissions = {
    'is_super_admin': is_super_admin,
    'is_admin': is_admin,
    'is_user_itself': is_user_itself,
    'auth_required': auth_required
}


def is_multiple(data):
    if isinstance(data, list):
        return True
    if isinstance(data, str):
        if data.find(",") > 0:
            return True
    return False


def permission_manager(view, view_args, view_kwargs, *args, **kwargs):
    """The function use to check permissions

    :param callable view: the view
    :param list view_args: view args
    :param dict view_kwargs: view kwargs
    :param list args: decorator args
    :param dict kwargs: decorator kwargs
    """
    methods = 'GET,POST,DELETE,PATCH'

    if 'id' in kwargs:
        view_kwargs['id'] = kwargs['id']

    if 'methods' in kwargs:
        methods = kwargs['methods']

    if request.method not in methods:
        return view(*view_args, **view_kwargs)

    # leave_if checks if we have to bypass this request on the basis of lambda function
    if 'leave_if' in kwargs:
        check = kwargs['leave_if']
        if check(view_kwargs):
            return view(*view_args, **view_kwargs)

    # A check to ensure it is good to go ahead and check permissions
    if 'check' in kwargs:
        check = kwargs['check']
        if not check(view_kwargs):
            return ForbiddenError({'source': ''}, 'Access forbidden').respond()

    # leave_if checks if we have to bypass this request on the basis of lambda function
    if 'leave_if' in kwargs:
        check = kwargs['leave_if']
        if check(view_kwargs):
            return view(*view_args, **view_kwargs)

    # # If event_identifier in route instead of event_id
    # if 'event_identifier' in view_kwargs:
    #     try:
    #         event = Event.query.filter_by(identifier=view_kwargs['event_identifier']).one()
    #     except NoResultFound as e:
    #         return NotFoundError({'parameter': 'event_identifier'}, 'Event not found').respond()
    #     view_kwargs['event_id'] = event.id

    # # Only for events API
    # if 'identifier' in view_kwargs:
    #     try:
    #         event = Event.query.filter_by(identifier=view_kwargs['identifier']).one()
    #     except NoResultFound as e:
    #         return NotFoundError({'parameter': 'identifier'}, 'Event not found').respond()
    #     view_kwargs['id'] = event.id

    if 'fetch' in kwargs:
        fetched = None
        if is_multiple(kwargs['fetch']):
            kwargs['fetch'] = [f.strip() for f in kwargs['fetch'].split(",")]
            for f in kwargs['fetch']:
                if f in view_kwargs:
                    fetched = view_kwargs.get(f)
                    break
        elif kwargs['fetch'] in view_kwargs:
            fetched = view_kwargs[kwargs['fetch']]
        if not fetched:
            model = kwargs['model']
            fetch = kwargs['fetch']
            # fetch_as = kwargs['fetch_as']
            fetch_key_url = 'id'
            fetch_key_model = 'id'
            if 'fetch_key_url' in kwargs:
                fetch_key_url = kwargs['fetch_key_url']

            if 'fetch_key_model' in kwargs:
                fetch_key_model = kwargs['fetch_key_model']

            if not is_multiple(model):
                model = [model]

            if is_multiple(fetch_key_url):
                fetch_key_url = fetch_key_url.split(",")

            found = False
            for index, mod in enumerate(model):
                if is_multiple(fetch_key_url):
                    f_url = fetch_key_url[index].strip()
                else:
                    f_url = fetch_key_url
                if not view_kwargs.get(f_url):
                    continue
                try:
                    data = mod.query.filter(
                        getattr(mod, fetch_key_model) == view_kwargs[f_url]).one()
                except NoResultFound:
                    pass
                else:
                    found = True
                    break

            if not found:
                return NotFoundError({'source': ''}, 'Object not found.').respond()

            fetched = None
            if is_multiple(fetch):
                for f in fetch:
                    if hasattr(data, f):
                        fetched = getattr(data, f)
                        break
            else:
                fetched = getattr(data, fetch) if hasattr(
                    data, fetch) else None

        if fetched:
            kwargs[kwargs['fetch_as']] = fetched
        else:
            return NotFoundError({'source': ''}, 'Object not found.').respond()

    if args[0] in permissions:
        return permissions[args[0]](view, view_args, view_kwargs, *args, **kwargs)
    else:
        return ForbiddenError({'source': ''}, 'Access forbidden').respond()


def has_access(access_level, **kwargs):
    """
    The method to check if the logged in user has specified access
    level or nor
    :param string access_level: name of access level
    :param dict kwargs: This is directly passed to permission manager
    :return: bool: True if passes the access else False
    """
    if access_level in permissions:
        auth = permissions[access_level](
            lambda *a, **b: True, (), {}, (), **kwargs)
        if isinstance(auth, bool) and auth is True:
            return True
    return False
