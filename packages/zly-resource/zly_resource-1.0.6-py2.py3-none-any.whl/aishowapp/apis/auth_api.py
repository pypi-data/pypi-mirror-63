# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import json

from flask import request, jsonify, g
from flask_restful import Api, Resource, reqparse

from aishowapp.ext import db
from aishowapp.models.rbac import User, UserSearch
from aishowapp.until import require_frequency

UserApi = Api(prefix='/user')

# # //处理登录
class Login(Resource):
    def get(self,user_id=None):
        return {'code':200,}
    def post(self):
        username=request.json['username']
        password=request.json['password']
        # username=request.form['username']
        # password=request.form['password']
        print(request.args)
        print(username,password)
        user_obj=User.query.filter(User.username == username,User.password == password ).first()
        # print(User.queryToDict(user_obj))
        if user_obj:
            g.name = username
            token=hashlib.md5(username.encode('utf8')).hexdigest()
            try:
                user_obj.token = token
                db.session.commit()
                # print('ok')
            except Exception as e:
                db.session.rollback()
                print(e)
            return jsonify({'code':20000,'data':{'token':token}})
        else:
            return jsonify({'code': 50008, 'data': {'message':'用户名密码不正确,请重新登陆','token': 'admin-token'}})

# # //返回用户的信息
class UserInfo(Resource):
    def get(self):
        # print(request.args.to_dict())
        args_dict=request.args.to_dict()
        # print(args_dict)
        user_obj = User.query.filter(User.token==args_dict['token']).first()
        print(user_obj)
        usersearch_count = UserSearch.query.filter(UserSearch.user_id==user_obj.id).count()
        print('usersearch_count',usersearch_count)
        res_dict=User.queryToDict(user_obj)
        if usersearch_count:
            res_dict['question']=usersearch_count
        else:
            res_dict['question']=None
        # print(user_obj)
        # print(user_obj.roles)
        # for role in user_obj.roles:
        #     print(role.permissions)
        # print( [item.r_name for item in user_obj.roles])
        res_dict['roles']= [item.r_name for item in user_obj.roles]
        per_list=[role.permissions for role in user_obj.roles]
        # print(per_list)
        # print(per_list[0])
        res_dict['perms']= [perm.p_url for perm in per_list[0]]
        # res_dict['perms']=['/aishow/list']
        print(res_dict)
        return {'code':20000,'data':res_dict}

# # //注销登录
class Logout(Resource):
    def post(self):
        # print(request.args.to_dict())
        return {'code':20000,'data':'success'}

#问题界面
class Question(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('name', type=str)
        self.parse.add_argument('lessage', type=int)
        self.parse.add_argument('moreage', type=int)
        self.parse.add_argument('goods_category', type=str)
        self.parse.add_argument('lessprice', type=int)
        self.parse.add_argument('moreprice', type=int)
        self.parse.add_argument('tag', type=str)
        self.parse.add_argument('city', type=str)
        self.parse.add_argument('sex', type=str)
        self.args = self.parse.parse_args()
        g.name = self.args.get('name')

    @require_frequency
    def get(self):
        print('question')
        print(self.args)
        user = User.query.filter(User.username == self.args['name']).first()
        usersearch_totle = UserSearch.query.join(User).filter(User.username == self.args['name']).count()
        usersearch_obj_all = UserSearch.query.join(User).filter(User.username == self.args['name']).all()
        usersearch_obj_1 = UserSearch.query.join(User).filter(User.username == self.args['name']).first()
        print('usersearch_obj_1',usersearch_obj_1)
        print('usersearch_obj_all',usersearch_obj_all)
        usersearch = UserSearch()
        if usersearch_totle == 3:
            db.session.delete(usersearch_obj_1)
            db.session.commit()
        usersearch.conditions = json.dumps(self.args,ensure_ascii='utf8')
        usersearch.count = usersearch_totle+1
        usersearch.time = datetime.now()
        usersearch.user_id = user.id
        usersearch.save(usersearch)
        return {'code':20000,'data':'success'}

    def post(self):
        args = self.parse.parse_args()
        return {'code': 20000, 'data': 'success'}


UserApi.add_resource(Login,'/login')
UserApi.add_resource(Question,'/question')
UserApi.add_resource(UserInfo,'/info')
UserApi.add_resource(Logout,'/logout')