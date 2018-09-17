# -*- coding: utf-8 -*-

from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.responses.geokrety_types import \
    GeokretyTypesResponse
from tests.unittests.utils.responses.move import MoveResponse
from tests.unittests.utils.responses.moves_types import MovesTypesResponse
from tests.unittests.utils.responses.news import NewsResponse
from tests.unittests.utils.responses.news_comment import NewsCommentResponse
from tests.unittests.utils.responses.news_subscription import \
    NewsSubscriptionResponse
from tests.unittests.utils.responses.user import UserResponse


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

    def assertRaiseJsonApiError(self, pointer):
        """Assert an error response has a specific pointer
        """
        assert 'errors' in self
        for error in self['errors']:
            assert 'source' in error
            assert 'pointer' in error['source']
            if pointer in error['source']['pointer']:
                return True
        assert False, "JsonApiError pointer '{}' not raised".format(pointer)  # pragma: no cover


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


class NewsCommentCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(NewsCommentCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(NewsCommentResponse(data_))
        self['data'] = datas


class GeokretyTypesCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(GeokretyTypesCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(GeokretyTypesResponse(data_))
        self['data'] = datas


class MovesCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(MovesCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(MoveResponse(data_))
        self['data'] = datas


class MovesTypesCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(MovesTypesCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(MovesTypesResponse(data_))
        self['data'] = datas


class UsersCollectionResponse(BaseCollectionResponse):

    def __init__(self, data):
        super(UsersCollectionResponse, self).__init__(data)
        datas = []
        for data_ in self.data:
            datas.append(UserResponse(data_))
        self['data'] = datas
