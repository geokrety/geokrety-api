# -*- coding: utf-8 -*-

from base import BaseResponse


class GeokretResponse(BaseResponse):

    @property
    def holder(self):
        self._get_attribute('holder')
