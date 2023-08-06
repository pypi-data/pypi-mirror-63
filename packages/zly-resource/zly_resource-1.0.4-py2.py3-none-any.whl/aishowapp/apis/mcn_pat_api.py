# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Api, Resource, reqparse

from aishowapp.ext import db
from aishowapp.models.ai_star import KolList
from aishowapp.models.mcn_pat import Mcn, PlatForm
from aishowapp.models.rbac import User

McnPatApi = Api(prefix='/aishow/list')

#达人的增删改查
class NewExportADUC(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('broker', type=str)
        self.parse.add_argument('nickname', type=str)
        self.parse.add_argument('name', type=str)
        self.parse.add_argument('platform_id', type=str)
        self.parse.add_argument('way', type=str)
        self.parse.add_argument('sex', type=bool)
        self.parse.add_argument('fans', type=int)
        self.parse.add_argument('viewers', type=int)
        self.parse.add_argument('Online', type=int)
        self.parse.add_argument('region', type=str)
        self.parse.add_argument('commission', type=int)
        self.parse.add_argument('attributes', type=str)
        self.parse.add_argument('price', type=int)
        self.parse.add_argument('invoicing', type=bool)
        self.parse.add_argument('live_url', type=str)
        self.parse.add_argument('brand', type=str)
        self.parse.add_argument('data', type=str)
        self.parse.add_argument('gent', type=str)
        self.parse.add_argument('mcn_id', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('sort', type=str)
        self.args = self.parse.parse_args()

    def get(self):
        print('mcn get args', self.args)
        try:
            # User.username.like("%" + self.args['broker'] + "%") if self.args['broker'] is not None else "").first()

            if self.args['nickname']:
                mcn_query = Mcn.query.filter(KolList.nickname.like("%" + self.args['nickname'] + "%") if self.args['nickname'] is not None else "").offset((int(self.args['page']) - 1) * int(self.args['limit'])).limit(
                    int(self.args['limit'])).all()
                totle = Mcn.query.filter(KolList.nickname.like("%" + self.args['nickname'] + "%") if self.args['nickname'] is not None else "").count()
            else:
                mcn_query = Mcn.query.offset((int(self.args['page']) - 1) * int(self.args['limit'])).limit(
                    int(self.args['limit'])).all()
                totle = Mcn.query.count()
            if mcn_query:
                mcn_dict = Mcn.queryToDict(mcn_query)
            else:
                mcn_dict=[]
            # print(mcn_dict)
            return jsonify({'code': 20000, 'data': {'total': totle, 'items': mcn_dict }})
        except Exception as e:
            print('e', e)

    def post(self):
        print('mcn post args',self.args)
        mcn = self.add_updata()
        print('sada',mcn.sex)
        print('ok5')
        try:
            mcn.save(mcn)
            print('ok6')
            mcn_query = Mcn.query.offset((int(self.args['page']) - 1) * int(self.args['limit'])).limit(
                int(self.args['limit'])).all()
            print('ok7')
            totle = Mcn.query.count()
            mcn_dict = Mcn.queryToDict(mcn_query)
            return jsonify({'code': 20000, 'data': {'total': totle, 'items': mcn_dict}})
        except Exception as e:
            print('e', e)

    def put(self):
        print('mcn put args',self.args)
        mcn = self.add_updata()
        try:
            mcn.save(mcn)
            mcn_query = Mcn.query.offset((int(self.args['page']) - 1) * int(self.args['limit'])).limit(
                int(self.args['limit'])).all()
            totle = Mcn.query.count()
            mcn_dict = Mcn.queryToDict(mcn_query)
            return jsonify({'code': 20000, 'data': {'total': totle, 'items': mcn_dict}})
        except Exception as e:
            print('e', e)

    def delete(self):
        print('mcn delete args', self.args)
        mcn_obj = Mcn.query.filter(Mcn.id == self.args['user_id']).first()

        if mcn_obj:
            try:
                db.session.delete(mcn_obj)
                db.session.commit()
            except Exception as e:
                print('e', e)
        mcn_query = Mcn.query.offset((int(self.args['page']) - 1) * int(self.args['limit'])).limit(
            int(self.args['limit'])).all()
        totle = Mcn.query.count()
        mcn_dict = Mcn.queryToDict(mcn_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': mcn_dict}})

    def add_updata(self):
        mcn = Mcn()
        print(type(self.args['fans']))
        mcn.nickname = self.args['nickname']
        mcn.name = self.args['name']
        mcn.way = self.args['way']
        mcn.sex = self.args['sex']
        mcn.fans = self.args['fans']
        mcn.viewers = self.args['viewers']
        mcn.Online = self.args['Online']
        mcn.region = self.args['region']
        mcn.commission = self.args['commission']
        mcn.attributes = self.args['attributes']
        mcn.price = self.args['price']
        mcn.invoicing = self.args['invoicing']
        mcn.live_url = self.args['live_url']
        mcn.brand = self.args['brand']
        mcn.data = self.args['data']
        mcn.mcn_id = self.args['mcn_id']
        print('ok1')
        if self.args['broker']:
            broker_query = User.query.filter(
                User.username.like("%" + self.args['broker'] + "%") if self.args['broker'] is not None else "").first()
            if broker_query:
                print('ok2')
                print(broker_query.id)
                mcn.broker = broker_query.id

        if self.args['platform_id']:
            platform_query = PlatForm.query.filter(
                PlatForm.name.like("%" + self.args['platform_id'] + "%") if self.args['platform_id'] is not None else "").first()
            if platform_query:
                print('ok3')
                print(platform_query.id)
                mcn.platform_id = platform_query.id
        if self.args['gent']:
            gent_query = User.query.filter(
                User.username.like("%" + self.args['gent'] + "%") if self.args['gent'] is not None else "").first()
            if gent_query:
                print('ok4')
                print(gent_query.id)
                mcn.gent = gent_query.id

        return mcn


McnPatApi.add_resource(NewExportADUC, '/newexportaduc')