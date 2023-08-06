# -*- coding: utf-8 -*-
from datetime import datetime
import json
import time
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy import and_


from aishowapp.models.ai_star import PhoneAgeInfo, ShoppingCart, FansAttribute, KolList, Ebusines
from aishowapp.models.rbac import UserSearch, User

ShowApi = Api(prefix='/aishow/list')

# # //联网的电商数据
class NewExport(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('week', type=str)
        self.parse.add_argument('month', type=str)
        self.parse.add_argument('like', type=str)
        self.parse.add_argument('username', type=str)
        self.parse.add_argument('nickname', type=str)
        self.parse.add_argument('search', type=str)
    def get(self):
        args = self.parse.parse_args()
        # pagination = KolList.query.paginate(int(args['page']),int(args['limit']), error_out=False)
        # print(1,pagination)
        # print(2,pagination.items)
        # print(3,pagination.query)
        # print(4,pagination.pages)
        # print(5,pagination.total )
        # print(args)
        try:
            totle,res_aishow = self.search(**args)
            return jsonify({'code':20000,'data':{'total':totle,'items': res_aishow}})
        except Exception as e:
            print('e', e)
    def search(self,**kwargs):
        print(kwargs)
        conditions=[]
        if kwargs.get('search', None):
            print('search')
            if kwargs.get('nickname', None):
                conditions.append(
                    KolList.nickname.like("%" + kwargs['nickname'] + "%") if kwargs['nickname'] is not None else "")
            else:
                if kwargs.get('tag',None) or kwargs.get('like',None) :
                    if kwargs['tag'] == '全部'or kwargs.get('tag',None) =='0' :
                        pass
                    elif kwargs.get('tag', None) != '0':
                        # conditions.append(or_(KolList.tag==kwargs['tag'],KolList.tag==kwargs['like']) )
                        conditions.append(KolList.tag == kwargs['tag'])
                    # else :
                    #     conditions.append(KolList.tag == kwargs['like'] )
                if kwargs.get('week', None):
                    print('week')
                    week_list = kwargs['week'].split('--')
                    week_timestrip_less= time.mktime(time.strptime(week_list[1], '%Y/%m/%d'))
                    week_timestrip_more= time.mktime(time.strptime(week_list[0], '%Y/%m/%d'))
                    print(week_timestrip_less,week_timestrip_more)
                    week_datatime_less = datetime.fromtimestamp(week_timestrip_less)
                    week_datatime_more = datetime.fromtimestamp(week_timestrip_more)
                    print(week_datatime_less,week_datatime_more,type(week_datatime_more))
                    conditions.append(KolList.c_time.between(week_datatime_less,week_datatime_more))
                if kwargs.get('month',None):
                    month_list = kwargs['month'].split('--')
                    month_timestrip_less = time.mktime(time.strptime(month_list[1], '%Y/%m/%d'))
                    month_timestrip_more = time.mktime(time.strptime(month_list[0], '%Y/%m/%d'))
                    month_datatime_less = datetime.fromtimestamp(month_timestrip_less)
                    month_datatime_more = datetime.fromtimestamp(month_timestrip_more)
                    conditions.append(KolList.c_time.between(month_datatime_less,month_datatime_more))
            result_tuple = KolList.query.filter(and_(*conditions)).order_by(KolList.follower_num.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
            int(kwargs['limit'])).all()
            totle = KolList.query.filter(*conditions).count()
        else:
            print('no search')

            usersearch = UserSearch.query.join(User).filter(User.username==kwargs.get('username')).order_by(UserSearch.time.desc()).first()
            print('usersearch',usersearch)
            # print('usersearch.conditions',usersearch.conditions,type(usersearch.conditions))
            usersearch_dict = json.loads(usersearch.conditions)
            print('usersearch.conditions',json.loads(usersearch.conditions),type(json.loads(usersearch.conditions)))
            if usersearch_dict:
                print('ok')
                if usersearch_dict.get and usersearch_dict.get:
                    print('ok1')
                    print(type(usersearch_dict.get))
                    conditions.append(KolList.age.between(usersearch_dict['lessage'], usersearch_dict['moreage']))
                if usersearch_dict.get and usersearch_dict.get != '全部':
                    print('ok2')
                    conditions.append(KolList.tag == usersearch_dict.get)
                if usersearch_dict.get and usersearch_dict.get != '全部':
                    print('ok3')
                    conditions.append(KolList.sex == usersearch_dict.get)
                result_tuple = KolList.query.join(PhoneAgeInfo).filter(and_(*conditions)).order_by(getattr(PhoneAgeInfo, usersearch_dict['city']).desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
            int(kwargs['limit'])).all()
                print('result_tuple')
                totle = KolList.query.filter(*conditions).count()
                print('totle',totle)
        print('2222',*conditions)
        print(result_tuple)
        if result_tuple:
            result_dict = KolList.queryToDict(result_tuple)
        else:
            result_dict=[]
        return totle,result_dict

#  获取潜力达人
class TopExport(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('heat', type=int)
        self.parse.add_argument('lessfans', type=int)
        self.parse.add_argument('morefans', type=int)
        self.parse.add_argument('nickname', type=str)
        self.parse.add_argument('week', type=str)
        self.parse.add_argument('month', type=str)
        self.parse.add_argument('search', type=str)
        # self.parse.add_argument('message', type=str)

    def get(self):
        args = self.parse.parse_args()
        print(args)
        try:
            totle,res_aishow = self.search(**args)
            return jsonify({'code':20000,'data':{'total':totle,'items': res_aishow}})
        except Exception as e:
            print('e',e)
    def search(self,**kwargs):
        conditions=[]
        if kwargs.get('search', None):
            print('search')
            if kwargs.get('nickname', None):
                conditions.append(
                    KolList.nickname.like("%" + kwargs['nickname'] + "%") if kwargs['nickname'] is not None else "")
            else:
                if kwargs.get('tag',None):
                    if kwargs['tag']=='全部' or kwargs.get('tag', None) == '0':
                        pass
                    elif kwargs.get('tag', None) != '0':
                        conditions.append(KolList.tag == kwargs['tag'])
                if kwargs.get('lessfans') and kwargs.get('morefans'):
                    conditions.append(
                        KolList.follower_num.between(int(kwargs['lessfans']), int(kwargs['morefans'])))
                if kwargs.get('week', None):
                    # print('week')
                    week_list = kwargs['week'].split('--')
                    week_timestrip_less = time.mktime(time.strptime(week_list[1], '%Y/%m/%d'))
                    week_timestrip_more = time.mktime(time.strptime(week_list[0], '%Y/%m/%d'))
                    # print(week_timestrip_less, week_timestrip_more)
                    week_datatime_less = datetime.fromtimestamp(week_timestrip_less)
                    week_datatime_more = datetime.fromtimestamp(week_timestrip_more)
                    # print(week_datatime_less, week_datatime_more, type(week_datatime_more))
                    conditions.append(KolList.c_time.between(week_datatime_less, week_datatime_more))
                if kwargs.get('month', None):
                    month_list = kwargs['month'].split('--')
                    month_timestrip_less = time.mktime(time.strptime(month_list[1], '%Y/%m/%d'))
                    month_timestrip_more = time.mktime(time.strptime(month_list[0], '%Y/%m/%d'))
                    month_datatime_less = datetime.fromtimestamp(month_timestrip_less)
                    month_datatime_more = datetime.fromtimestamp(month_timestrip_more)
                    conditions.append(KolList.c_time.between(month_datatime_less, month_datatime_more))

            result_tuple = KolList.query.filter(*conditions).order_by(KolList.follower_num.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
            int(kwargs['limit'])).all()
            totle = KolList.query.filter(*conditions).count()
        else:
            print('no search')
            usersearch = UserSearch.query.order_by(UserSearch.time.desc()).first()
            print('usersearch.conditions', usersearch.conditions, type(usersearch.conditions))
            usersearch_dict = json.loads(usersearch.conditions)
            print('usersearch.condition', json.loads(usersearch.conditions), type(json.loads(usersearch.conditions)))
            if usersearch_dict:
                print('ok')
                if usersearch_dict.get and usersearch_dict.get:
                    conditions.append(KolList.age.between(int(usersearch_dict['lessage']), int(usersearch_dict['moreage'])))
                if usersearch_dict.get and usersearch_dict.get != '全部':
                    conditions.append(KolList.tag == usersearch_dict.get)
                if usersearch_dict.get and usersearch_dict.get != '全部':
                    conditions.append(KolList.sex == usersearch_dict.get)
                result_tuple = KolList.query.join(PhoneAgeInfo).filter(and_(*conditions)).order_by(
                    getattr(PhoneAgeInfo, usersearch_dict['city']).desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
            int(kwargs['limit'])).all()
                totle = KolList.query.count()
                print('totle',totle)
        # print(result_tuple)
        if result_tuple:
            result_dict = KolList.queryToDict(result_tuple)
        else:
            result_dict=[]
        return totle,result_dict

# # //联网的电商数据
class NewEbusiness(Resource):
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
        self.parse.add_argument('Sales_volume', type=str)
        self.parse.add_argument('sell_price', type=str)
        self.parse.add_argument('userid',type=str)
    def get(self):
        print('ebusiness_get')
        args = self.parse.parse_args()
        print(args)
        print('')
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})
    def search(self,**kwargs):
        # print(kwargs)
        print(kwargs['userid'])
        conditions=[]
        if kwargs.get('userid',None):
            result_tuple=Ebusines.query.join(KolList).filter(KolList.userid == kwargs['userid']).order_by(
                Ebusines.datatime.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle =Ebusines.query.join(KolList).filter(KolList.userid == kwargs['userid']).count()
        else:

            result_tuple = Ebusines.query.order_by(Ebusines.datatime.desc()).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
                int(kwargs['limit'])).all()
            totle = Ebusines.query.count()
        if result_tuple:
            result_dict = Ebusines.queryToDict(result_tuple)
        else:
            result_dict=[]
        print(result_dict)
        return totle,result_dict

# 粉丝详情
class NewFans(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=str)
        self.parse.add_argument('limit', type=str)
        self.parse.add_argument('userid',type=str)

    def get(self):
        print('fans_get')
        args = self.parse.parse_args()
        print(args)
        totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_aishow}})

    def search(self,**kwargs):
        # print(kwargs)
        # print(kwargs['userid'])
        result_dict_list=[]
        if kwargs.get('userid', None):
            result_phoneageInfo=PhoneAgeInfo.query.join(KolList).filter(KolList.userid == kwargs['userid']).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle_phoneageInfo = PhoneAgeInfo.query.join(KolList).filter(KolList.userid == kwargs['userid']).count()
            result_shoppingcart = ShoppingCart.query.join(KolList).filter(KolList.userid == kwargs['userid']).offset((int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(
                int(kwargs['limit'])).all()
            # print('result_shoppingcart', result_shoppingcart)
            totle_shoppingcart = ShoppingCart.query.join(KolList).filter(KolList.userid == kwargs['userid']).count()
            result_fansattribute = FansAttribute.query.join(KolList).filter(KolList.userid == kwargs['userid']).offset(
                (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle_fansattribute = FansAttribute.query.count()
            if result_phoneageInfo:
                print('result_phoneageInfo',result_phoneageInfo)
                phoneageInfo_dict = PhoneAgeInfo.queryToDict(result_phoneageInfo)
            else:
                phoneageInfo_dict=[]
            if result_shoppingcart:
                print('result_shoppingcart',result_shoppingcart)
                shoppingcart_dict = ShoppingCart.queryToDict(result_shoppingcart)
            else:
                shoppingcart_dict = []
            if result_fansattribute:
                print('result_fansattribute',result_fansattribute)
                fansattribute_dict = FansAttribute.queryToDict(result_fansattribute)
            else:
                fansattribute_dict = []
            print('ok')
            print(phoneageInfo_dict,type(phoneageInfo_dict))
            print(shoppingcart_dict,type(shoppingcart_dict))
            print(fansattribute_dict,type(fansattribute_dict))

            result_dict_list=phoneageInfo_dict+shoppingcart_dict+fansattribute_dict
            totle = totle_phoneageInfo + totle_shoppingcart + totle_fansattribute
        else:
            result_dict_list=[]
            totle=0
        print(result_dict_list)
        print(totle)
        return totle,result_dict_list

# 词云详情--未做
class NewOthers(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('fansdescription', type=str)

    def get(self):
        print('Others_get')
        args = self.parse.parse_args()
        print(args, type(args))
        data={}
        l1 = args['fansdescription'].split('_')
        data['fans_sex'] = l1[0]
        l2 = l1[1].split(',')
        data['fans_region'] = l2[0]
        data['fans_city'] = l2[1]
        l3 = l1[2].split(',')
        data['fans_phone'] = l3[0]
        data['fans_shop'] = l3[1]
        print(data)
        # totle, res_aishow = self.search(**args)
        return jsonify({'code': 20000, 'data': data})


# 绑定路由
ShowApi.add_resource(NewExport,'/newexport')
ShowApi.add_resource(TopExport,'/topexport')
ShowApi.add_resource(NewFans,'/newfans')
ShowApi.add_resource(NewEbusiness,'/newebusiness')
ShowApi.add_resource(NewOthers,'/newothers')




