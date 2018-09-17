from flask import request
from flask_jwt import current_identity
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from app.api.helpers.data_layers import MOVE_TYPE_COMMENT
from app.api.helpers.exceptions import ForbiddenException
from app.api.helpers.permissions import jwt_required
from app.models.geokret import Geokret
from app.models.move import Move


# @jwt_required
def is_anonymous(view, view_args, view_kwargs, *args, **kwargs):
    if current_identity._get_current_object() is not None:
        raise ForbiddenException('Anonymous access is required', {'source': 'id'})


@jwt_required
def auth_required(view, view_args, view_kwargs, *args, **kwargs):
    return True


@jwt_required
def is_admin(view, view_args, view_kwargs, *args, **kwargs):
    user = current_identity
    if not user.is_admin:
        raise ForbiddenException('Admin access is required', {'source': 'id'})
    return True


@jwt_required
def is_user_itself(view, view_args, view_kwargs, *args, **kwargs):
    """
    Allows admin and super admin access to any resource irrespective of id.
    Otherwise the user can only access his/her resource.
    """
    user = current_identity
    if not user.is_admin and str(user.id) != str(kwargs['user_id']):
        raise ForbiddenException('Access Forbidden', {'source': 'user_id'})
    return True


@jwt_required
def is_move_author(view, view_args, view_kwargs, *args, **kwargs):
    """
    Allows Move author to fully manage move.
    """
    user = current_identity
    if user.is_admin:
        return True

    try:
        move = Move.query.filter(Move.id == kwargs['move_id']).one()
    except NoResultFound:  # pragma: no cover
        raise ObjectNotFound('Move not found.', {'source': 'move_id'})

    if move.author_id == user.id:
        return True

    raise ForbiddenException('Access denied.', {'source': 'move_id'})


@jwt_required
def is_geokret_owner(view, view_args, view_kwargs, *args, **kwargs):
    """
    Allows GeoKret owner access to private resources of owned GeoKrety.
    Otherwise the user can only access public resource.
    """
    user = current_identity
    if user.is_admin:
        return True

    try:
        geokret = Geokret.query.filter(Geokret.id == kwargs['geokret_id']).one()
    except NoResultFound:  # pragma: no cover
        raise ObjectNotFound('Geokret not found.', {'source': 'geokret_id'})

    if geokret.owner_id == user.id:
        return True

    raise ForbiddenException('Access denied.', {'source': 'geokret_id'})


@jwt_required
def is_geokret_holder(view, view_args, view_kwargs, *args, **kwargs):
    user = current_identity
    if user.is_admin:
        return True

    try:
        geokret = Geokret.query.filter(Geokret.id == kwargs['geokret_id']).one()
    except NoResultFound:  # pragma: no cover
        raise ObjectNotFound('Geokret not found.', {'source': 'geokret_id'})

    if geokret.holder_id == current_identity.id:
        return True

    raise ForbiddenException('Not the GeoKret holder.', {'source': 'geokret_id'})


@jwt_required
def has_touched_geokret(view, view_args, view_kwargs, *args, **kwargs):
    user = current_identity
    if user.is_admin:  # pragma: no cover
        return True

    try:
        geokret = Geokret.query.filter(Geokret.id == kwargs['geokret_id']).one()
    except NoResultFound:  # pragma: no cover
        raise ObjectNotFound('Geokret not found.', {'source': 'geokret_id'})

    if Move.query \
            .filter(Move.geokret_id == geokret.id) \
            .filter(Move.author_id == user.id) \
            .filter(Move.type != MOVE_TYPE_COMMENT).count() > 0:
        return True

    raise ForbiddenException('Has never touched the GeoKret.', {'source': 'geokret_id'})


permissions = {
    'is_anonymous': is_anonymous,
    'is_admin': is_admin,
    'is_user_itself': is_user_itself,
    'auth_required': auth_required,
    'is_geokret_owner': is_geokret_owner,
    'is_geokret_holder': is_geokret_holder,
    'is_move_author': is_move_author,
    'has_touched_geokret': has_touched_geokret,
}


def is_multiple(data):  # pragma: no cover
    if isinstance(data, list):
        return True
    if isinstance(data, str):
        if data.find(",") > 0:
            return True
    return False


def permission_manager(view, view_args, view_kwargs, *args, **kwargs):  # pragma: no cover
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
        return

    # leave_if checks if we have to bypass this request on the basis of lambda function
    if 'leave_if' in kwargs:
        check = kwargs['leave_if']
        if check(view_kwargs):
            return

    # A check to ensure it is good to go ahead and check permissions
    if 'check' in kwargs:
        check = kwargs['check']
        if not check(view_kwargs):
            raise ForbiddenException('Access forbidden', {'source': ''})

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
                raise ObjectNotFound('Object not found.', {'source': ''})

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
            raise ObjectNotFound('Object not found.', {'source': ''})

    if args[0] in permissions:
        permissions[args[0]](view, view_args, view_kwargs, *args, **kwargs)
    else:
        raise ForbiddenException('Access forbidden', {'source': ''})


def has_access(access_level, **kwargs):
    """
    The method to check if the logged in user has specified access
    level or nor
    :param string access_level: name of access level
    :param dict kwargs: This is directly passed to permission manager
    :return: bool: True if passes the access else False
    """
    try:
        if access_level in permissions:
            permissions[access_level](lambda *a, **b: True, (), {}, (), **kwargs)
    except Exception:
        return False
    return True
