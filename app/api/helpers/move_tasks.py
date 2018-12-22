import geopy.distance
import requests

from app import current_app, make_celery
from app.api.helpers.data_layers import (MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN)
from app.models.geokret import Geokret
from app.models.move import Move

celery = make_celery(current_app)


@celery.task(name='update.move.distance')
def update_move_distances(geokret_id):
    """ Recompute and update all moves distances for a GeoKret
    """
    moves = Move.query.filter(Move.geokret_id == geokret_id).order_by(Move.moved_on_datetime.asc())
    geokret = Geokret.query.get(geokret_id)

    last = None
    for move in moves:
        # updates the last_position_id which is the ruch_id for last log of type grabbed, dropped, met or archived
        if move.type in (MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN, MOVE_TYPE_ARCHIVED):
            geokret.last_position_id = move.id
        geokret.last_move_id = move.id
        if move.latitude is None:
            continue
        if last is None:
            last = move
            continue

        distance = geopy.distance.distance((last.latitude, last.longitude), (move.latitude, move.longitude)).km
        move.distance = int(round(distance))
        geokret.distance += move.distance
        last = move


@celery.task(name='update.move.country.and.elevation')
def update_move_country_and_altitude(move_id):
    """ Obtain and update country and altitude of a move
    """
    move = Move.query.get(move_id)

    if move.latitude is not None and move.longitude is not None:
        response = requests.get('https://geo.kumy.org/api/getCountry?lat={}&lon={}'.format(move.latitude, move.longitude))
        if response.ok:
            move.country = response.text
        else:
            move.country = 'XYZ'

        response = requests.get('https://geo.kumy.org/api/getElevation?lat={}&lon={}'.format(move.latitude, move.longitude))
        if response.ok and response.text != 'None':
            move.altitude = response.text
        else:
            move.altitude = '-2000'
    else:
        move.country = ''
        move.altitude = -32768


@celery.task(name='update.geokret.total.moves.count')
def update_geokret_total_moves_count(geokret_id):
    """ Update GeoKret total move count
    """
    moves = Move.query \
        .filter(Move.geokret_id == geokret_id) \
        .filter(Move.type.in_((MOVE_TYPE_DROPPED, MOVE_TYPE_SEEN, MOVE_TYPE_DIPPED))) \
        .order_by(Move.moved_on_datetime.desc())

    geokret = Geokret.query.get(geokret_id)
    geokret.caches_count = moves.count()


@celery.task(name='update.geokret.holder')
def update_geokret_holder(geokret_id):
    """ Update GeoKret holder
    """
    moves = Move.query \
        .filter(Move.geokret_id == geokret_id) \
        .filter(Move.type != MOVE_TYPE_COMMENT) \
        .order_by(Move.moved_on_datetime.desc())

    geokret = Geokret.query.get(geokret_id)

    geokret.holder_id = None
    if moves.count():
        for move in moves:
            if move.type in [MOVE_TYPE_DROPPED, MOVE_TYPE_ARCHIVED, MOVE_TYPE_SEEN]:
                break
            elif move.type in [MOVE_TYPE_GRABBED, MOVE_TYPE_DIPPED]:
                geokret.holder_id = move.author_id
                break
