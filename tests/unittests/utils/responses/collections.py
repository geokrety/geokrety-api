# -*- coding: utf-8 -*-

import pprint

from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.responses.news import NewsResponse


class BaseCollectionResponse(dict):

    def __init__(self, data):
        self.update(data)

    @property
    def data(self):
        assert 'data' in self
        return self['data']

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
