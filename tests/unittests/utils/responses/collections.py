# -*- coding: utf-8 -*-

import pprint

from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.responses.geokrety_types import GeokretyTypesResponse
from tests.unittests.utils.responses.news import NewsResponse
from tests.unittests.utils.responses.news_subscription import NewsSubscriptionResponse


class BaseCollectionResponse(dict):

    def __init__(self, data):
        self.update(data)

    @property
    def data(self):
        return self.get('data', [])

    @property
    def count(self):
        return self['meta']['count']

    def assertCount(self, count):
        assert self.count == count

    def pprint(self):
        pprint.pprint(self)


class GeokretCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(GeokretCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(GeokretResponse(data_))
        self['data'] = datas


class NewsCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(NewsCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(NewsResponse(data_))
        self['data'] = datas


class NewsSubscriptionCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(NewsSubscriptionCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(NewsSubscriptionResponse(data_))
        self['data'] = datas



class GeokretyTypesCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(GeokretyTypesCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(GeokretyTypesResponse(data_))
        self['data'] = datas
