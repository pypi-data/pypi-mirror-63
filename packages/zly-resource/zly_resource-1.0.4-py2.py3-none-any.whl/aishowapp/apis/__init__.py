# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(sys.modules['__main__'])

from aishowapp.apis.auth_api import UserApi
from aishowapp.apis.goods_api import GoodsApi
from aishowapp.apis.mcn_pat_api import McnPatApi
from aishowapp.apis.rbac_api import RbacApi
from aishowapp.apis.search_api import SearchApi
from aishowapp.apis.show_api import ShowApi
from aishowapp.apis.resource_api import ResourceApi
# from aishowapp.apis.paltformliveshow_api import PaltformApi


def init_api(app):
    ShowApi.init_app(app)
    UserApi.init_app(app)
    GoodsApi.init_app(app)
    McnPatApi.init_app(app)
    RbacApi.init_app(app)
    SearchApi.init_app(app)
    ResourceApi.init_app(app)
    # PaltformApi.init_app(app)

