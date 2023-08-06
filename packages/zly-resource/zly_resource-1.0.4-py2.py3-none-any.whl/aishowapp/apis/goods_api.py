# -*- coding: utf-8 -*-
import datetime
import json
import time

from flask import jsonify
from flask_restful import Api, Resource, reqparse

from aishowapp.models.ai_star import Ebusines, KolList, PhoneAgeInfo
from aishowapp.models.rbac import UserSearch

GoodsApi = Api(prefix='/aigoods/list')


# //电商带货数据
class Ebusiness(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('search', type=str)
        self.parse.add_argument('Commodity_classification', type=str)
        self.parse.add_argument('goods_category', type=str)

    def get(self):
        print('ebusiness_get')
        args = self.parse.parse_args()
        print(args)
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})

    def search(self, **kwargs):
        conditions = []
        if kwargs.get('search', None):
            print('search')
            if kwargs.get('Commodity_classification', None):
                conditions.append(
                    Ebusines.Commodity_classification.like("%" + kwargs['Commodity_classification'] + "%") if kwargs[
                                                                                                                  'Commodity_classification'] is not None else "")
            else:
                if kwargs.get('goods_category', None):
                    if kwargs['goods_category'] != '0':
                        conditions.append(Ebusines.goods_category == kwargs['goods_category'])
        else:
            print('no search')
            usersearch = UserSearch.query.order_by(UserSearch.time.desc()).first()
            # print('usersearch.condition', usersearch.conditions, type(usersearch.conditions))
            usersearch_dict = json.loads(usersearch.conditions)
            print('usersearch.conditions', json.loads(usersearch.conditions),
                  type(json.loads(usersearch.conditions)))
            if usersearch_dict:
                if usersearch_dict.get('goods_category') and usersearch_dict.get('goods_category') != '全部':
                    conditions.append(Ebusines.goods_category == usersearch_dict.get('goods_category'))
                if usersearch_dict.get('lessprice') and usersearch_dict.get('moreprice'):
                    conditions.append(Ebusines.sell_price.between(int(usersearch_dict['lessprice']),
                                                                  int(usersearch_dict['moreprice'])))
        result_tuple = Ebusines.query.filter(*conditions).order_by(
            Ebusines.datatime.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
            int(kwargs['limit'])).all()
        totle = Ebusines.query.filter(*conditions).count()
        if result_tuple:
            result_dict = Ebusines.queryToDict(result_tuple)
        else:
            result_dict = []
        return totle, result_dict


# # //达人电商带货数据
class ExportEbusiness(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=str)
        self.parse.add_argument('limit', type=str)
        self.parse.add_argument('data', type=str)
        self.parse.add_argument('goods_category', type=str)
        self.parse.add_argument('Commodity_classification', type=str)
        self.parse.add_argument('Video_likes', type=str)
        self.parse.add_argument('Video_count', type=str)
        self.parse.add_argument('Total_browsing', type=str)
        self.parse.add_argument('sales_volume', type=str)
        self.parse.add_argument('sell_price', type=str)
        self.parse.add_argument('userid', type=str)

    def get(self):
        print('ebusiness_get')
        args = self.parse.parse_args()
        print(args)
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})

    def search(self, **kwargs):
        # print(kwargs)
        print(kwargs['userid'])
        result_dict = []
        conditions = []
        if kwargs.get('userid', None):
            result_tuple = Ebusines.query.join(KolList).filter(KolList.userid == kwargs['userid']).order_by(
                Ebusines.datatime.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
                int(kwargs['limit'])).all()
            totle = Ebusines.query.join(KolList).filter(KolList.userid == kwargs['userid']).count()
        else:
            result_tuple = Ebusines.query.order_by(Ebusines.datatime.desc()).offset(
                (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
                int(kwargs['limit'])).all()
            totle = Ebusines.query.count()
        if result_tuple:
            result_dict = Ebusines.queryToDict(result_tuple)
        print(result_dict)
        return totle, result_dict


# # //抖音达人销售榜
class Douyinexportsell(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=str)
        self.parse.add_argument('limit', type=str)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('month', type=str)
        self.parse.add_argument('week', type=str)
        self.parse.add_argument('goods_category', type=str)
        self.parse.add_argument('nickname', type=str)
        self.parse.add_argument('search', type=str)
        self.parse.add_argument('lessprice', type=int)
        self.parse.add_argument('moreprice', type=int)
        self.parse.add_argument('lesssell', type=int)
        self.parse.add_argument('moresell', type=int)
        self.parse.add_argument('search', type=str)

    def get(self):
        print('Douyinexportsell')
        args = self.parse.parse_args()
        print(args)
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})

    def search(self, **kwargs):
        conditions = []
        if kwargs.get('search', None):
            print('search')
            if kwargs.get('nickname', None):
                conditions.append(
                    KolList.nickname.like("%" + kwargs['nickname'] + "%") if kwargs['nickname'] is not None else "")
            else:
                if kwargs.get('week', None):
                    print('week')
                    week_list = kwargs['week'].split('--')
                    week_timestrip_less = time.mktime(time.strptime(week_list[1], '%Y/%m/%d'))
                    week_timestrip_more = time.mktime(time.strptime(week_list[0], '%Y/%m/%d'))
                    print(week_timestrip_less, week_timestrip_more)
                    week_datatime_less = datetime.fromtimestamp(week_timestrip_less)
                    week_datatime_more = datetime.fromtimestamp(week_timestrip_more)
                    print(week_datatime_less, week_datatime_more, type(week_datatime_more))
                    conditions.append(KolList.c_time.between(week_datatime_less, week_datatime_more))
                if kwargs.get('month', None):
                    month_list = kwargs['month'].split('--')
                    month_timestrip_less = time.mktime(time.strptime(month_list[1], '%Y/%m/%d'))
                    month_timestrip_more = time.mktime(time.strptime(month_list[0], '%Y/%m/%d'))
                    month_datatime_less = datetime.fromtimestamp(month_timestrip_less)
                    month_datatime_more = datetime.fromtimestamp(month_timestrip_more)
                    conditions.append(KolList.c_time.between(month_datatime_less, month_datatime_more))
                if kwargs.get('tag', None) or kwargs.get('like', None):
                    if kwargs['tag'] == '全部':
                        pass
                    elif kwargs.get('tag', None) and kwargs.get('tag', None) != '0':
                        conditions.append(KolList.tag == kwargs['tag'])
                    else:
                        conditions.append(KolList.tag == kwargs['like'])
                if kwargs.get('goods_category', None):
                    if kwargs['goods_category'] == '全部' or kwargs['goods_category'] == '0':
                        pass
                    else:
                        conditions.append(Ebusines.commodity_category == kwargs['goods_category'])
                if kwargs.get('lessprice') and kwargs.get('moreprice'):
                    conditions.append(
                        Ebusines.sell_price.between(kwargs['lessprice'], kwargs['moreprice']))
                if kwargs.get('lesssell') and kwargs.get('moresell'):
                    conditions.append(
                        Ebusines.Sales_volume.between(kwargs['lesssell'], kwargs['moresell']))
            result_tuple = Ebusines.query.join(KolList).filter(*conditions).order_by(
                Ebusines.Total_browsing.desc()).offset(
                (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle = Ebusines.query.join(KolList).filter(*conditions).count()
        else:
            print('no search')
            usersearch = UserSearch.query.order_by(UserSearch.time.desc()).first()
            # print('usersearch.conditions', usersearch.conditions, type(usersearch.conditions))
            usersearch_dict = json.loads(usersearch.conditions)
            print('usersearch.conditions', json.loads(usersearch.conditions),
                  type(json.loads(usersearch.conditions)))
            if usersearch_dict:
                if usersearch_dict.get('lessprice') and usersearch_dict.get('moreprice'):
                    conditions.append(
                        Ebusines.sell_price.between(usersearch_dict['lessprice'], usersearch_dict['moreprice']))
                if usersearch_dict.get('lessage') and usersearch_dict.get('moreage'):
                    conditions.append(
                        KolList.age.between(usersearch_dict['lessage'], usersearch_dict['moreage']))
                if usersearch_dict.get('goods_category') and usersearch_dict.get('goods_category') != '全部':
                    conditions.append(Ebusines.goods_category == usersearch_dict.get('goods_category'))
                if usersearch_dict.get('tag') and usersearch_dict.get('tag') != '全部':
                    conditions.append(KolList.tag == usersearch_dict.get('tag'))
                if usersearch_dict.get('sex') and usersearch_dict.get('sex') != '全部':
                    conditions.append(KolList.sex == usersearch_dict.get('sex'))
                # if usersearch_dict.get('city', None):
                # reiontest_obj_list = PhoneAgeInfo.query.order_by(getattr(PhoneAgeInfo, usersearch_dict['city']).desc()).all()
                #                     # reiontest_id_list = [KolList.queryToDict(item.kolList)['userid'] for item in reiontest_obj_list]
                #                     # conditions.append(KolList.userid.in_(reiontest_id_list))
                #                     # print(*conditions)
                result_tuple = Ebusines.query.join(KolList, KolList.userid == Ebusines.userid).join(PhoneAgeInfo,
                                                                                                    Ebusines.userid == PhoneAgeInfo.userid).filter(
                    *conditions) \
                    .order_by(getattr(PhoneAgeInfo, usersearch_dict['city']).desc()).offset(
                    (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
                totle = Ebusines.query.join(KolList).filter(*conditions).count()
        # print(result_tuple)
        res_dict = []
        if result_tuple:
            result_dict = Ebusines.queryToDict(result_tuple)
            for item in result_dict:
                kollist_obj = KolList.query.filter(KolList.userid == item['userid']).first()
                kollist_obj_dict = KolList.queryToDict(kollist_obj)
                kollist_obj_dict.update(item)
                res_dict.append(kollist_obj_dict)
            return totle, res_dict
        return totle, res_dict


# # //抖音达人直播榜
class Douyinexportview(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('nickname', type=str)
        self.parse.add_argument('search', type=str)

    def get(self):
        print('Douyinexportview_get')
        args = self.parse.parse_args()
        print(args)
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})

    def search(self, **kwargs):
        conditions = []
        if kwargs.get('search', None):
            print('search')
            if kwargs.get('nickname', None):
                conditions.append(
                    KolList.nickname.like("%" + kwargs['nickname'] + "%") if kwargs['nickname'] is not None else "")
            else:
                if kwargs.get('tag', None) or kwargs.get('like', None):
                    if kwargs['tag'] == '全部' or kwargs.get('tag', None) == '0':
                        pass
                    else:
                        conditions.append(KolList.tag == kwargs['tag'])
                    # else :
                    # conditions.append(KolList.tag == kwargs['like'])
            result_tuple = Ebusines.query.join(KolList).filter(*conditions).order_by(
                KolList.follower_num.desc()).offset(
                (kwargs['page'] - 1) * kwargs['limit']).limit(kwargs['limit']).all()
            totle = Ebusines.query.join(KolList).filter(*conditions).count()
        else:
            print('no search')
            usersearch = UserSearch.query.order_by(UserSearch.time.desc()).first()
            print('usersearch.conditions', usersearch.conditions, type(usersearch.conditions))
            usersearch_dict = json.loads(usersearch.conditions)
            print('usersearch.condition', json.loads(usersearch.conditions), type(json.loads(usersearch.conditions)))
            if usersearch_dict:
                if usersearch_dict.get('lessprice') and usersearch_dict.get('moreprice'):
                    conditions.append(
                        Ebusines.sell_price.between(usersearch_dict['lessprice'], usersearch_dict['moreprice']))
                if usersearch_dict.get('lessage') and usersearch_dict.get('moreage'):
                    conditions.append(
                        KolList.age.between(usersearch_dict['lessage'], usersearch_dict['moreage']))
                if usersearch_dict.get('goods_category') and usersearch_dict.get('goods_category') != '全部':
                    conditions.append(Ebusines.goods_category == usersearch_dict.get('goods_category'))
                if usersearch_dict.get('tag') and usersearch_dict.get('tag') != '全部':
                    conditions.append(KolList.tag == usersearch_dict.get('tag'))
                if usersearch_dict.get('sex') and usersearch_dict.get('sex') != '全部':
                    conditions.append(KolList.sex == usersearch_dict.get('sex'))
                print('*conditions', *conditions)
                result_tuple = Ebusines.query.join(KolList, KolList.userid == Ebusines.userid).join(PhoneAgeInfo,
                                                                                                    KolList.userid == PhoneAgeInfo.userid).filter(
                    *conditions).order_by(getattr(PhoneAgeInfo, usersearch_dict['city']).desc()).offset(
                    (kwargs['page'] - 1) * kwargs['limit']).limit(kwargs['limit']).all()
                result_tuple1 = Ebusines.query.join(KolList, KolList.userid == Ebusines.userid).join(PhoneAgeInfo,
                                                                                                     KolList.userid == PhoneAgeInfo.userid).filter(
                    *conditions).offset((kwargs['page'] - 1) * kwargs['limit']).limit(kwargs['limit']).all()
                totle = Ebusines.query.join(KolList).join(PhoneAgeInfo).filter(*conditions).count()
            print('result_tuple', result_tuple)
            print('result_tuple1', result_tuple1)
        res_dict = []
        if result_tuple:
            result_dict = Ebusines.queryToDict(result_tuple)
            for item in result_dict:
                kollist_obj = KolList.query.filter(KolList.userid == item['userid']).first()
                kollist_obj_dict = KolList.queryToDict(kollist_obj)
                kollist_obj_dict.update(item)
                res_dict.append(kollist_obj_dict)
            return totle, res_dict
        return totle, res_dict

GoodsApi.add_resource(Ebusiness,'/ebusiness')
GoodsApi.add_resource(ExportEbusiness,'/exportebusiness')
GoodsApi.add_resource(Douyinexportview,'/douyinexportview')
GoodsApi.add_resource(Douyinexportsell,'/douyinexportsell')
