from app.api.helpers.data_layers import GeoKretyTypeDataLayer
from app.api.schema.geokrety_types import GeoKretyTypesSchema
from flask_rest_jsonapi import ResourceDetail, ResourceList


class GeokretTypeList(ResourceList):

    methods = ['GET']
    schema = GeoKretyTypesSchema
    data_layer = {
        'class': GeoKretyTypeDataLayer
    }


class GeokretTypeDetail(ResourceDetail):

    methods = ['GET']
    schema = GeoKretyTypesSchema
    data_layer = {
        'class': GeoKretyTypeDataLayer
    }
