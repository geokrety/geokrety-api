import requests

import geopy.distance
from app import current_app, make_celery
from app.models import db
from app.models.geokret import Geokret
from app.models.move import Move

from sqlalchemy.sql import func

celery = make_celery(current_app)


@celery.task(name='update.move.distance')
def update_move_distances(geokret_id):
    """ Recompute and update all moves distances for a GeoKret
    """
    moves = Move.query.filter(Move.geokret_id == geokret_id).order_by(Move.moved_on_date_time.asc())

    last = None
    for move in moves:
        if move.latitude is None:
            continue
        if last is None:
            last = move
            continue

        distance = geopy.distance.distance((last.latitude, last.longitude), (move.latitude, move.longitude)).km
        move.distance = int(round(distance))
        last = move


@celery.task(name='update.move.country.and.elevation')
def update_country_and_altitude(move_id):
    """ Obtain and update country and altitude of a move
    """
    move = Move.query.get(move_id)

    response = requests.get('https://geo.kumy.org/api/getCountry?lat={}&lon={}'.format(move.latitude, move.longitude))
    if response.ok:
        move.country = response.text
    else:
        move.country = 'XYZ'

    response = requests.get('https://geo.kumy.org/api/getElevation?lat={}&lon={}'.format(move.latitude, move.longitude))
    if response.ok:
        move.altitude = response.text
    else:
        move.altitude = '-2000'


@celery.task(name='update.geokret.distance')
def update_geokret_total_distance(geokret_id):
    """ Update GeoKret total distance
    """
    distance = db.session.query(func.sum(Move.distance)) \
        .filter(Move.geokret_id == geokret_id).one()

    geokret = Geokret.query.get(geokret_id)
    geokret.distance = distance


@celery.task(name='update.geokret.total.moves.count')
def update_geokret_total_moves_count(geokret_id):
    """ Update GeoKret total move count
    """
