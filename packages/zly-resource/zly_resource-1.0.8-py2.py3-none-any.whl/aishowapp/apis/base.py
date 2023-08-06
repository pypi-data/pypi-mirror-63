# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from six.moves.urllib.parse import urljoin

import requests
import json


class BaseAPI(object):

    _http = requests.Session()

    API_BASE_URL = 'http://47.110.58.200:8081/api/v1.0/'

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        from aishowapp.baseclient import BaseClient
        bsc = BaseClient()
        self._client = bsc
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self.post(url, data, params, **kwargs)

    def get(self, uri, params=None, **kwargs):
        """
        get 接口请求

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        """
        if params is not None:
            kwargs['params'] = params  #====> kwargs={'params':{'select_type':select_type,'page':page,'limit':limit}}
        return self.request('GET', uri, **kwargs)
    def post(self, uri, data=None, params=None, **kwargs):
        """
        post 接口请求

        :param uri: 请求url
        :param data: post 数据（dict 格式会自动转换为json）
        :param params: post接口中url问号后参数（dict 格式）
        """
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)
    # 对request进行封装
    def request(self, method, uri, **kwargs):
        # 将基础路径和试图函数拼接成完整的访问路劲
        if not uri.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, uri)
            print('对request进行封装  url ', url)
        else:
            url = uri
            print('对request进行封装  url ', url)

        # 判断是否有params参数，
        if 'params' not in kwargs:
            kwargs['params'] = {}
        # 判断是否有data参数，
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body
            # 判断是否有headers参数，
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/json'

        # 发送requests.Session()的request()请求
        result = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        return result

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
