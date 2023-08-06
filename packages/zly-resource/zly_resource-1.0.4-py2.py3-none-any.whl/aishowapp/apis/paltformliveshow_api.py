# # -*- coding: utf-8 -*-
# import json
#
# from flask import jsonify
# from flask_restful import Api, Resource, reqparse
#
# # from aishowapp.models.resource_model import DouyinViewExport, RedbookImageTextLink, DouyinSpecialLive, \
# #     DouyinSingleChainLive, TaobaoLive, KuaiShouLive, QitengTaobaoExportLiveOffer, QitengRedbookPrice, \
# #     QitengDouyinViewPrice, ResourceTable
#
# PaltformApi = Api(prefix='/platformresource/list')
#
# #抖音短视频达人表
# class DouyinShortViewShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get',args)
#         try:
#             dyve_query = DouyinViewExport.query.offset((args['page'] - 1) * args['limit']).limit(args['limit']).all()
#             res_dict = []
#             totle = DouyinViewExport.query.count()
#             if dyve_query:
#                 all_dict = DouyinViewExport.queryToDict(dyve_query)
#                 print()
#                 for item in all_dict:
#                     r_query = ResourceTable.query.filter(ResourceTable.id == item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict=[]
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict }},ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict }})
#         except Exception as e:
#             print('e', e)
#
# #小红书图文链接
# class RedbookImageTextLinkShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get',args)
#         try:
#             dyve_query = RedbookImageTextLink.query.offset((args['page'] - 1) * args['limit']).limit(args['limit']).all()
#             res_dict = []
#             totle = RedbookImageTextLink.query.count()
#             if dyve_query:
#                 all_dict = RedbookImageTextLink.queryToDict(dyve_query)
#                 print()
#                 for item in all_dict:
#                     r_query = ResourceTable.query.filter(ResourceTable.id == item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict=[]
#             # print(mcn_dict)
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict}}, ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict }})
#         except Exception as e:
#             print('e', e)
#
# #抖音专场直播
# class DouyinSpecialLiveShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get', args)
#         try:
#             dyve_query = DouyinSpecialLive.query.offset((args['page'] - 1) * args['limit']).limit(
#                 args['limit']).all()
#             res_dict = []
#             totle = DouyinSpecialLive.query.count()
#             if dyve_query:
#                 all_dict = DouyinSpecialLive.queryToDict(dyve_query)
#                 for item in all_dict:
#                     r_query=ResourceTable.query.filter(ResourceTable.id==item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict = []
#             # print(mcn_dict)
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict}}, ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})
#         except Exception as e:
#             print('e', e)
#
# #抖音单链直播
# class DouyinSingleChainLiveShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get', args)
#
#         try:
#             dyve_query = DouyinSingleChainLive.query.offset((args['page'] - 1) * args['limit']).limit(
#                 args['limit']).all()
#             res_dict = []
#             totle = DouyinSingleChainLive.query.count()
#             if dyve_query:
#                 all_dict = DouyinSingleChainLive.queryToDict(dyve_query)
#                 for item in all_dict:
#                     r_query = ResourceTable.query.filter(ResourceTable.id == item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict = []
#             # print(mcn_dict)
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict}}, ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})
#         except Exception as e:
#             print('e', e)
#
# #淘宝直播
# class TaobaoLiveShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get', args)
#
#         try:
#             dyve_query = TaobaoLive.query.offset((args['page'] - 1) * args['limit']).limit(
#                 args['limit']).all()
#             res_dict = []
#             totle = TaobaoLive.query.count()
#             if dyve_query:
#                 all_dict = TaobaoLive.queryToDict(dyve_query)
#                 for item in all_dict:
#                     r_query = ResourceTable.query.filter(ResourceTable.id == item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict = []
#             # print(mcn_dict)
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict}}, ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})
#         except Exception as e:
#             print('e', e)
#
# # 快手直播
# class KuaiShouLiveShow(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('resourcetable args get', args)
#         try:
#             dyve_query = KuaiShouLive.query.offset((args['page'] - 1) * args['limit']).limit(
#                 args['limit']).all()
#             res_dict = []
#             totle = KuaiShouLive.query.count()
#             if dyve_query:
#                 all_dict = KuaiShouLive.queryToDict(dyve_query)
#                 for item in all_dict:
#                     r_query = ResourceTable.query.filter(ResourceTable.id == item['resource_table_id']).first()
#                     if r_query:
#                         r_dict = ResourceTable.queryToDict(r_query)
#                         r_dict.update(item)
#                         res_dict.append(r_dict)
#             else:
#                 res_dict = []
#             print(res_dict)
#             print(json.dumps({'code': 20000, 'data': {'total': totle, 'items': res_dict}}, ensure_ascii=False))
#             return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})
#         except Exception as e:
#             print('e', e)
#
# PaltformApi.add_resource(DouyinShortViewShow, '/douyinshortview')
# PaltformApi.add_resource(RedbookImageTextLinkShow, '/redbookimagetextlink')
# PaltformApi.add_resource(DouyinSpecialLiveShow, '/douyinspeciallive')
# PaltformApi.add_resource(DouyinSingleChainLiveShow, '/douyinsingllive')
# PaltformApi.add_resource(TaobaoLiveShow, '/taobaolive')
# PaltformApi.add_resource(KuaiShouLiveShow, '/kuaishoulive')




