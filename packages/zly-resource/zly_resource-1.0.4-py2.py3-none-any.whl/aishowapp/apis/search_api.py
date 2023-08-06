# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Api, Resource, reqparse

from aishowapp.models.ai_star import KolList, Region

SearchApi = Api(prefix='/aisearch/list')

class MoreSearchExport(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('lessfans', type=int)
        self.parse.add_argument('morefans', type=int)
        self.parse.add_argument('lessinteraction_15', type=int)
        self.parse.add_argument('moreinteraction_15', type=int)
        self.parse.add_argument('lessvido', type=int)
        self.parse.add_argument('morevido', type=int)
        self.parse.add_argument('lessage', type=int)
        self.parse.add_argument('moreage', type=int)
        self.parse.add_argument('sex', type=str)
        self.parse.add_argument('city', type=str)

    def get(self):
        args = self.parse.parse_args()
        print(args)
        try:
            totle,res_aishow = self.search(**args)
            return jsonify({'code':20000,'data':{'total':totle,'items': res_aishow}})
        except Exception as e:
            print('e',e)

    def search(self,**kwargs):
        # print(kwargs)
        conditions=[]
        if kwargs.get('tag',None):
            if kwargs['tag'] == '全部':
                pass
            else:
                conditions.append(KolList.tag == kwargs['tag'])
        if kwargs.get('lessfans') and kwargs.get('morefans'):
            conditions.append(
                KolList.follower_num.between(int(kwargs['lessfans']), int(kwargs['morefans'])))
        if kwargs.get('lessinteraction_15') and kwargs.get('morefans'):
            conditions.append(
                KolList.avg_interaction_15.between(int(kwargs['lessinteraction_15']), int(kwargs['moreinteraction_15'])))
        if kwargs.get('lessvido') and kwargs.get('morevido'):
            conditions.append(
                KolList.video_count.between(int(kwargs['lessvido']), int(kwargs['morevido'])))
        if kwargs.get('lessage') and kwargs.get('moreage'):
            conditions.append(
                KolList.age.between(int(kwargs['lessage']), int(kwargs['moreage'])))
        if kwargs.get('sex',None):
            if kwargs['sex'] =='全部':
                pass
            else:
                conditions.append(KolList.sex == kwargs['sex'])
        if kwargs.get('city',None) and  kwargs.get('city',None)!='全部':
            print('have city')
            result_tuple = KolList.query.join(Region).filter(*conditions).order_by(getattr(Region,kwargs['city']).desc()).offset(
                (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle = KolList.query.filter(*conditions).count()

        else:
            print('no city')
            print(*conditions)
            result_tuple = KolList.query.filter(*conditions).order_by(KolList.follower_num.desc()).offset(
                (int(kwargs['page']) - 1) * int(kwargs['limit'])).limit(int(kwargs['limit'])).all()
            totle = KolList.query.filter(*conditions).count()
        print(result_tuple)
        if result_tuple:
            result_dict = KolList.queryToDict(result_tuple)
        else:
            result_dict=[]
        return totle,result_dict


SearchApi.add_resource(MoreSearchExport,'/moresearchexport')