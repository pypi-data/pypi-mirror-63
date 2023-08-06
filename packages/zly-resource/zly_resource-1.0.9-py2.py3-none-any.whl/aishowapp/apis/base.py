# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseAPI(object):

    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        from aishowapp.baseclient import BaseClient
        bsc = BaseClient()
        self._client = bsc
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        from aishowapp.baseclient import BaseClient
        bsc = BaseClient()
        self._client = bsc
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, data, params, **kwargs)

    @classmethod
    def get_datas(self, request, model=None):

        headers = request.headers
        content_type = headers.get
        print(content_type)
        if request.method == "GET":
            return request.args
        if content_type == 'application/x-www-form-urlencoded':
            print("1")
            return request.form
        if content_type.startswith('application/json'):
            print("2")
            return request.get_json()

        content_type_list = str(content_type).split(';')
        if len(content_type_list) > 0:
            if content_type_list[0] == 'multipart/form-data':
                print("3")
                return request.form
