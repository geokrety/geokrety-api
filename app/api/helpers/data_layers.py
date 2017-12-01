from flask_rest_jsonapi.data_layers.base import BaseDataLayer

GEOKRETY_TYPES = [
    {'id': 0, 'name': 'Traditional'},
    {'id': 1, 'name': 'A book/CD/DVD'},
    {'id': 2, 'name': 'A Human'},
    {'id': 3, 'name': 'A coin'},
    {'id': 4, 'name': 'KretyPost'},
]
GEOKRETY_TYPES_COUNT = 5

MOVE_TYPES = [
    {'id': 0, 'name': 'Dropped to'},
    {'id': 1, 'name': 'Grabbed from'},
    {'id': 2, 'name': 'A comment'},
    {'id': 3, 'name': 'Seen in'},
    {'id': 4, 'name': 'Archived'},
    {'id': 5, 'name': 'Visiting'},
]
MOVE_TYPES_COUNT = 6


class GeoKretyTypeDataLayer(BaseDataLayer):

    def get_object(self, view_kwargs):
        """Retrieve an object
        :params dict view_kwargs: kwargs from the resource view
        :return DeclarativeMeta: an object
        """
        try:
            return GEOKRETY_TYPES[view_kwargs['id']]
        except IndexError:
            return None

    def get_collection(self, qs, view_kwargs):
        """Retrieve a collection of objects
        :param QueryStringManager qs: a querystring manager to retrieve information from url
        :param dict view_kwargs: kwargs from the resource view
        :return tuple: the number of object and the list of objects
        """
        return GEOKRETY_TYPES_COUNT, GEOKRETY_TYPES


class MovesTypeDataLayer(BaseDataLayer):

    def get_object(self, view_kwargs):
        """Retrieve an object
        :params dict view_kwargs: kwargs from the resource view
        :return DeclarativeMeta: an object
        """
        try:
            return MOVE_TYPES[view_kwargs['id']]
        except IndexError:
            return None

    def get_collection(self, qs, view_kwargs):
        """Retrieve a collection of objects
        :param QueryStringManager qs: a querystring manager to retrieve information from url
        :param dict view_kwargs: kwargs from the resource view
        :return tuple: the number of object and the list of objects
        """
        return MOVE_TYPES_COUNT, MOVE_TYPES
