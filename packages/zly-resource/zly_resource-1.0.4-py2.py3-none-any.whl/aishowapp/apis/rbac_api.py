# -*- coding: utf-8 -*-
from flask_restful import Api, Resource

RbacApi = Api(prefix='/admin/')

class Roles(Resource):
    def get(self):
        roles = [{'key': 'admin',
                  'name': 'admin',
                  'description': 'Super Administrator. Have access to view all pages.',
                  '               routes': [{
                      'path': '',
                      'redirect': 'dashboard',
                      'children': [
                          {
                              'path': 'dashboard',
                              'name': 'Dashboard',
                              'meta': {'title': 'dashboard', 'icon': 'dashboard'}
                          }
                      ]
                  }]
                  },
                 {
                     'key': 'editor',
                     'name': 'editor',
                     'description': 'Normal Editor. Can see all pages except permission page',
                     'routes': [{
                         'path': '',
                         'redirect': 'dashboard',
                         'children': [
                             {
                                 'path': 'dashboard',
                                 'name': 'Dashboard',
                                 'meta': {'title': 'dashboard', 'icon': 'dashboard'}
                             }
                         ]
                     }]
                 },
                 {
                     'key': 'visitor',
                     'name': 'visitor',
                     'description': 'Just a visitor. Can only see the home page and the document page',
                     'routes': [{
                         'path': '',
                         'redirect': 'dashboard',
                         'children': [
                             {
                                 'path': 'dashboard',
                                 'name': 'Dashboard',
                                 'meta': {'title': 'dashboard', 'icon': 'dashboard'}
                             }
                         ]
                     }]
                 }
                 ]
        return {'code':20000,'data':roles}
    def post(self):
        pass

class Routes(Resource):
    def get(self):
        menuList = [
            {
                'id': 39,
                'title': 'it中心',
                'path': 'it',
                'parent_id': None,
            },
            {
                'id': 150,
                'title': 'it资产',
                'path': 'it',
                'parent_id': 39,
            },
            {
                'id': 151,
                'title': '资产管理',
                'path': 'it',
                'parent_id': 150,
            },
            {
                'id': 153,
                'title': '时段统计',
                'path': 'time',
                'parent_id': 152,
            },
        ]
        return {'code':20000,'data':menuList}
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass



RbacApi.add_resource(Roles,'/roles')
RbacApi.add_resource(Routes,'/routes')