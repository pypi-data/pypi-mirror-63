# -*- coding: utf-8 -*-
import json

from flask import jsonify
from flask_restful import Api, Resource, reqparse

from aishowapp.ext import db
from aishowapp.models.resource_model import DouyinSpecialLive, ResourceTable, DouyinSingleChainLive, DouyinViewExport, \
    KuaiShouLive, RedbookImageTextLink, TaobaoLive, QitengTaobaoExportLiveOffer, QitengRedbookPrice, \
    QitengDouyinViewPrice

ResourceApi = Api(prefix='/platformresource/list')


#达人的增删改查
class TotalResource(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('flag', type=str)
        self.parse.add_argument('select_type', type=int)
        self.parse.add_argument('kol_id', type=str)
        self.parse.add_argument('kol_name', type=str)
        self.parse.add_argument('platform', type=str)
        self.parse.add_argument('type_datil', type=str)
        self.parse.add_argument('company', type=str)
        self.parse.add_argument('contact_name', type=str)
        self.parse.add_argument('contact_phone', type=str)
        self.parse.add_argument('fans', type=float)
        self.parse.add_argument('status', type=str)

    def get(self):
        args = self.parse.parse_args()
        print('resourcetable args get',args)
        print('resourcetable args get',args['select_type'])
        all_list = []
        totle = 0
        #抖音专场直播
        if args['select_type'] == 1:
            dysl_query = DouyinSpecialLive.query.offset((args['page'] - 1) * args['limit']).limit(args['limit']).all()
            totle = DouyinSpecialLive.query.count()
            for item in dysl_query:
                dict = {}
                dict['dysl'] = DouyinSpecialLive.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                all_list.append(dict)
        #抖音单链接
        if args['select_type'] == 2:
            dyscl_query = DouyinSingleChainLive.query.offset((args['page'] - 1) * args['limit']).limit(args['limit']).all()
            totle = DouyinSingleChainLive.query.count()
            for item in dyscl_query:
                dict = {}
                dict['dyscl'] = DouyinSingleChainLive.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                all_list.append(dict)
        #抖音短视频
        if args['select_type'] == 3:
            dyscl_query = DouyinViewExport.query.offset((args['page'] - 1) * args['limit']).limit(
                args['limit']).all()
            totle = DouyinViewExport.query.count()
            for item in dyscl_query:
                dict = {}
                dict['dyve'] = DouyinViewExport.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                dysl2_query = QitengDouyinViewPrice.query.filter(QitengDouyinViewPrice.douyin_view_export_id == item.id).first()
                if dysl2_query:
                    dysl_dict = QitengDouyinViewPrice.queryToDict(dysl2_query)
                    dict['dyve']['child'] = {'qtdyvp': dysl_dict}
                all_list.append(dict)
        #快手直播
        if args['select_type'] == 4:
            dyscl_query = KuaiShouLive.query.offset((args['page'] - 1) * args['limit']).limit(
                args['limit']).all()
            totle = KuaiShouLive.query.count()
            for item in dyscl_query:
                dict = {}
                dict['ksl'] = KuaiShouLive.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                all_list.append(dict)
        #小红书图文链接
        if args['select_type'] == 5:
            dyscl_query = RedbookImageTextLink.query.offset((args['page'] - 1) * args['limit']).limit(
                args['limit']).all()
            totle = RedbookImageTextLink.query.count()
            for item in dyscl_query:
                dict = {}
                dict['rbitl'] = RedbookImageTextLink.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                dysl2_query = QitengRedbookPrice.query.filter(
                    QitengRedbookPrice.redbook_image_text_link_id ==  item.id).first()
                if dysl2_query:
                    dysl_dict = QitengDouyinViewPrice.queryToDict(dysl2_query)
                    dict['rbitl']['child'] = {'qtrbp': dysl_dict}
                all_list.append(dict)
        #淘宝直播
        if args['select_type'] == 6:
            dyscl_query = TaobaoLive.query.offset((args['page'] - 1) * args['limit']).limit(
                args['limit']).all()
            totle = TaobaoLive.query.count()
            for item in dyscl_query:
                dict = {}
                dict['tbl'] = TaobaoLive.queryToDict(item)
                res_query = item.resource_tables
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    print('res_dict',res_dict)
                    dict['rsst'] = res_dict
                dysl2_query = QitengTaobaoExportLiveOffer.query.filter(
                    QitengTaobaoExportLiveOffer.taobao_live_id == item.id).first()
                if dysl2_query:
                    dysl_dict = QitengTaobaoExportLiveOffer.queryToDict(dysl2_query)
                    dict['tbl']['child']={'qtrbp': dysl_dict}
                all_list.append(dict)
        # print('all_list',all_list)
        else:
            dict = {}
            rsst_query = ResourceTable.query.all()
            if rsst_query:
                res_dict = ResourceTable.queryToDict(rsst_query)
                print('res_dict', res_dict)
                dict['rsst'] = res_dict
                all_list.append(dict)
        print('all_list',json.dumps({'code': 20000, 'data': {'total': totle, 'items': all_list }},ensure_ascii=False))
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': all_list }})


    def post(self):
        print('resource post')
        args = self.parse.parse_args()
        res = self.add_updata(args)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [],'msg':'失败，请输入正确的数据'}})
        else:
        # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
        #     int(args['limit'])).all()
        # totle = ResourceTable.query.count()
        # res_dict = ResourceTable.queryToDict(res_query)
        #
            return self.get()

    def put(self):
        print('resource put')
        args = self.parse.parse_args()
        res = self.add_updata(args)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [],'msg':'更新失败，请输入正确的数据'}})
        else:
            return self.get()

    def delete(self):
        args = self.parse.parse_args()
        print('resourcetable delete args',args)
        res_obj = ResourceTable.query.filter(ResourceTable.id == int(args['user_id'])).first()
        res_id = res_obj.id
        print('res_id',res_id)
        flag = args.get
        if flag == '抖音专场直播':  # 抖音专场直播
            print('抖音专场直播')
            douyinsl_obj = DouyinSpecialLive.query.filter(DouyinSpecialLive.resource_table_id == res_id).first()
            if douyinsl_obj:
                try:
                    db.session.delete(douyinsl_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        elif flag == '抖音单链直播':  # 抖音专场直播
            print('抖音单链直播')
            douyinscl_obj = DouyinSingleChainLive.query.filter(DouyinSingleChainLive.resource_table_id == res_id).first()
            if douyinscl_obj:
                try:
                    db.session.delete(douyinscl_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        elif flag == '抖音短视频':  # 抖音专场直播
            print('抖音短视频')
            douyinve_obj = DouyinViewExport.query.filter(DouyinViewExport.resource_table_id == res_id).first()
            if douyinve_obj:
                try:
                    db.session.delete(douyinve_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        elif flag == '快手直播':  # 抖音专场直播
            print('快手直播')
            ks_obj = KuaiShouLive.query.filter(KuaiShouLive.resource_table_id == res_id).first()
            if ks_obj:
                try:
                    db.session.delete(ks_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        elif flag == '小红书图文链接':  # 抖音专场直播
            print('小红书图文链接')
            rebbookitl_obj = RedbookImageTextLink.query.filter(RedbookImageTextLink.resource_table_id == res_id).first()
            if rebbookitl_obj:
                try:
                    db.session.delete(rebbookitl_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        elif flag == '淘宝直播':  # 抖音专场直播
            print('淘宝直播')
            tbl_obj = TaobaoLive.query.filter(TaobaoLive.resource_table_id == res_id).first()
            if tbl_obj:
                try:
                    db.session.delete(tbl_obj)
                    db.session.commit()
                except Exception as e:
                    print('e', e)
        if res_obj:
            try:
                db.session.delete(res_obj)
                db.session.commit()
            except Exception as e:
                print('e', e)
        res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = ResourceTable.query.count()
        res_dict = ResourceTable.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def add_updata(self,args):
        status =args['status']
        if status=='create':
            rsourcetab = ResourceTable()
        else :
            rsourcetab = ResourceTable.query.filter(ResourceTable.kol_id==args['kol_id']).first()
        rsourcetab.kol_id = args.get
        rsourcetab.kol_name = args.get
        rsourcetab.platform = args.get
        rsourcetab.avatar = args.get
        rsourcetab.type_datil = args.get
        rsourcetab.company = args.get
        rsourcetab.contact_name = args.get
        rsourcetab.fans = args.get
        try:
            try:
                rsourcetab.save(rsourcetab)
            except Exception as e:
                print('TotalResource post except', e)
            resource_obj = ResourceTable.query.filter(ResourceTable.kol_id == args.get).all()[0]
            resource_id = resource_obj.id
            print(resource_id)
            flag = args.get
            if flag == '抖音专场直播':  # 抖音专场直播
                print('抖音专场直播')
                self.parse.add_argument('export_tag', type=str)
                self.parse.add_argument('special_offer', type=int)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('cooperation_case', type=str)
                self.parse.add_argument('douyin_special_cost_price', type=int)
                args1 = self.parse.parse_args()
                print('抖音专场直播 args1', args1)
                douyinsl = DouyinSpecialLive()
                douyinsl.resource_table_id = resource_id
                douyinsl.export_tag = args1.get
                douyinsl.special_offer = args1.get
                douyinsl.export_city = args1.get
                douyinsl.cooperation_case = args1.get
                douyinsl.douyin_special_cost_price = args1.get
                try:
                    douyinsl.save(douyinsl)
                    # dysl_query = DouyinSpecialLive.query.offset((args1['page']) - 1 * args1['limit']).limit(args1['limit']).all()
                    # print('ok7')
                    # totle = DouyinSpecialLive.query.count()
                    # dysl_dict = DouyinSpecialLive.queryToDict(dysl_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': dysl_dict}})
                except Exception as e:
                    print('DouyinSpecialLive save except', e)
            elif flag == '抖音单链直播':  # 抖音单链直播
                self.parse.add_argument('douyin_export_classification', type=str)
                self.parse.add_argument('Single_chain_offer', type=int)
                self.parse.add_argument('introduction', type=str)
                self.parse.add_argument('live_time', type=str)
                self.parse.add_argument('selection_requirements', type=str)
                self.parse.add_argument('remarks', type=str)
                self.parse.add_argument('douyin_single_cost_price', type=int)
                args = self.parse.parse_args()
                print('抖音单链直播',args)
                douyinscl = DouyinSingleChainLive()
                douyinscl.resource_table_id = resource_id
                douyinscl.douyin_export_classification = args.get
                douyinscl.Single_chain_offer = args.get
                douyinscl.introduction = args.get
                douyinscl.live_time = args.get
                douyinscl.selection_requirements = args.get
                douyinscl.remarks = args.get
                douyinscl.douyin_single_cost_price = args.get
                try:
                    douyinscl.save(douyinscl)
                    dyscl_query = DouyinSpecialLive.query.offset((args['page']) - 1 * args['limit']).limit(
                        args['limit']).all()
                    # totle = DouyinSingleChainLive.query.count()
                    # dyscl_dict = DouyinSingleChainLive.queryToDict(dyscl_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': dyscl_dict}})
                except Exception as e:
                    print('DouyinSpecialLive save except', e)
            elif flag == '抖音短视频':  # 抖音短视频
                self.parse.add_argument('export_tag', type=str)
                self.parse.add_argument('introduction', type=str)
                self.parse.add_argument('douyin_home_page', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('cooperation_case', type=str)
                self.parse.add_argument('better_sell_goods', type=str)
                self.parse.add_argument('douyin_export_classification', type=str)
                self.parse.add_argument('cooperation_mode', type=str)
                self.parse.add_argument('offer_less', type=int)
                self.parse.add_argument('offer_more', type=int)
                self.parse.add_argument('offer_less', type=int)
                self.parse.add_argument('star_offer', type=int)
                self.parse.add_argument('douyin_view_cost_price', type=int)
                args = self.parse.parse_args()
                douyinve = DouyinViewExport()
                douyinve.resource_table_id = resource_id
                douyinve.export_tag = args.get
                douyinve.introduction = args.get
                douyinve.douyin_home_page = args.get
                douyinve.export_city = args.get
                douyinve.cooperation_case = args.get
                douyinve.better_sell_goods = args.get
                douyinve.douyin_export_classification = args.get
                douyinve.cooperation_mode = args.get
                douyinve.offer_less = args.get
                douyinve.offer_more = args.get
                douyinve.star_offer = args.get
                douyinve.douyin_view_cost_price = args.get
                try:
                    douyinve.save(douyinve)
                    # dyve_query = DouyinViewExport.query.offset((args['page']) - 1 * args['limit']).limit(
                    #     args['limit']).all()
                    # totle = DouyinViewExport.query.count()
                    # dyve_dict = DouyinViewExport.queryToDict(dyve_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': dyve_dict}})
                except Exception as e:
                    print('DouyinViewExport save except', e)
            elif flag == '快手直播':  # 快手直播
                self.parse.add_argument('avg_online_num', type=float)
                self.parse.add_argument('sell_classification', type=str)
                self.parse.add_argument('commission_less', type=int)
                self.parse.add_argument('commission_more', type=int)
                self.parse.add_argument('attributes', type=str)
                self.parse.add_argument('better_sell_goods', type=str)
                self.parse.add_argument('kuaishou_offer', type=int)
                self.parse.add_argument('kuaishou_cost_price', type=int)
                self.parse.add_argument('remarks', type=str)
                args = self.parse.parse_args()
                ksl = KuaiShouLive()
                ksl.resource_table_id = resource_id
                ksl.avg_online_num = args.get
                ksl.sell_classification = args.get
                ksl.commission_less = args.get
                ksl.commission_more = args.get
                ksl.attributes = args.get
                ksl.kuaishou_offer = args.get
                ksl.kuaishou_cost_price = args.get
                ksl.remarks = args.get
                try:
                    ksl.save(ksl)

                    ksl_query = KuaiShouLive.query.offset((args['page']) - 1 * args['limit']).limit(
                        args['limit']).all()
                    # totle = KuaiShouLive.query.count()
                    # ksl_dict = KuaiShouLive.queryToDict(ksl_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': ksl_dict}})
                except Exception as e:
                    print('KuaiShouLive save except', e)
            elif flag == '小红书图文链接':  # 小红书图文链接
                print('抖音专场直播 args1')
                self.parse.add_argument('dianzan', type=int)
                self.parse.add_argument('redbook_link', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('export_tag', type=str)
                self.parse.add_argument('brand_partner', type=bool)
                self.parse.add_argument('redbook_cost_price', type=int)
                args = self.parse.parse_args()
                print('抖音专场直播 args1',args)
                rdltl = RedbookImageTextLink()
                rdltl.resource_table_id = resource_id
                rdltl.dianzan = args.get
                rdltl.redbook_link = args.get
                rdltl.export_city = args.get
                rdltl.export_tag = args.get
                rdltl.brand_partner = args.get
                rdltl.redbook_cost_price = args.get
                try:
                    rdltl.save(rdltl)
                    rdltl_query = RedbookImageTextLink.query.offset((args['page']) - 1 * args['limit']).limit(
                        args['limit']).all()
                    # totle = RedbookImageTextLink.query.count()
                    # rdltl_dict = RedbookImageTextLink.queryToDict(rdltl_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': rdltl_dict}})
                except Exception as e:
                    print('RedbookImageTextLink save except', e)
            elif flag == '淘宝直播':  # 淘宝直播
                print('抖音专场直播 args')
                self.parse.add_argument('avg_viewing_num', type=float)
                self.parse.add_argument('main_category', type=str)
                self.parse.add_argument('introduction', type=str)
                self.parse.add_argument('taobao_offer', type=int)
                self.parse.add_argument('taobao_cost_price', type=int)
                args = self.parse.parse_args()
                print('抖音专场直播 args1', args)
                tbl = TaobaoLive()
                tbl.resource_table_id = resource_id
                tbl.avg_viewing_num = args.get
                tbl.main_category = args.get
                tbl.introduction = args.get
                tbl.taobao_offer = args.get
                tbl.taobao_cost_price = args.get
                try:
                    tbl.save(tbl)
                    # tbl_query = TaobaoLive.query.offset((args['page']) - 1 * args['limit']).limit(
                    #     args['limit']).all()
                    # totle = TaobaoLive.query.count()
                    # tbl_dict = TaobaoLive.queryToDict(tbl_query)
                    # return jsonify({'code': 20000, 'data': {'total': totle, 'items': tbl_dict}})
                except Exception as e:
                    print('TaobaoLive save except', e)
        except Exception as e:
            db.session.rollback()
            print('TotalResource post except', e)
            return e


#麒腾淘宝KOL直播报价
class TaobaoExportLiveOffer(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('status', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('hierarchy', type=str)
        self.parse.add_argument('avg_viewing_num_less', type=float)
        self.parse.add_argument('avg_viewing_num_more', type=float)
        self.parse.add_argument('offer_less', type=int)
        self.parse.add_argument('offer_more', type=int)
        self.parse.add_argument('cost_price', type=str)
        self.parse.add_argument('remarks', type=str)
    def get(self):
        args = self.parse.parse_args()
        qttbelo_query = QitengTaobaoExportLiveOffer.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengTaobaoExportLiveOffer.query.count()
        if qttbelo_query:
            qttbelo_dict = QitengTaobaoExportLiveOffer.queryToDict(qttbelo_query)
        else:
            qttbelo_dict=[]
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})
    def post(self):

        args = self.parse.parse_args()
        print('qttbelo post args ', args)
        res = self.add_updata(args)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
        else:
            # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            #     int(args['limit'])).all()
            # totle = ResourceTable.query.count()
            # res_dict = ResourceTable.queryToDict(res_query)
            #
            return self.get()
    def put(self):

        args = self.parse.parse_args()
        print('qttbelo put args',args)
        res = self.add_updata(args)

        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})

        res_query = QitengTaobaoExportLiveOffer.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengTaobaoExportLiveOffer.query.count()
        res_dict = QitengTaobaoExportLiveOffer.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def delete(self):
        args = self.parse.parse_args()
        print('qttbelo delete args', args)
        qttbelo_obj = QitengTaobaoExportLiveOffer.query.filter(QitengTaobaoExportLiveOffer.id == int(args['user_id'])).first()

        if qttbelo_obj:
            try:
                db.session.delete(qttbelo_obj)
                db.session.commit()
            except Exception as e:
                print('e', e)
                return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
        res_query = QitengTaobaoExportLiveOffer.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengTaobaoExportLiveOffer.query.count()
        res_dict = QitengTaobaoExportLiveOffer.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def add_updata(self, args):
        status = args['status']
        if status == 'create':
            tbeloffer = QitengTaobaoExportLiveOffer()
            print('post create')
        else:
            tbeloffer = QitengTaobaoExportLiveOffer.query.filter(QitengTaobaoExportLiveOffer.id == int(args['user_id'])).first()
            print('put update',tbeloffer)
        tbeloffer.hierarchy = args.get
        tbeloffer.avg_viewing_num_less = args.get
        tbeloffer.avg_viewing_num_more = args.get
        tbeloffer.offer_less = args.get
        tbeloffer.offer_more = args.get
        tbeloffer.cost_price = args.get
        tbeloffer.remarks = args.get

        try:
            tbeloffer.save(tbeloffer)
        except Exception as e:
            db.session.rollback()
            print('TotalResource post except', e)
            return e



# 小红书报价
class RedbookPrice(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('status', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('fans_less', type=int)
        self.parse.add_argument('fans_more', type=int)
        self.parse.add_argument('cost_price', type=int)
        self.parse.add_argument('offer_less', type=int)
        self.parse.add_argument('offer_more', type=int)
        self.parse.add_argument('brand_partner', type=bool)


    def get(self):
        args = self.parse.parse_args()
        qttbelo_query = QitengRedbookPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengRedbookPrice.query.count()
        if qttbelo_query:
            qttbelo_dict = QitengRedbookPrice.queryToDict(qttbelo_query)
        else:
            qttbelo_dict = []
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})

    def post(self):

        args = self.parse.parse_args()
        print('qttbelo post args ', args)
        res = self.add_updata(args)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
        else:
            # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            #     int(args['limit'])).all()
            # totle = ResourceTable.query.count()
            # res_dict = ResourceTable.queryToDict(res_query)
            #
            return self.get()

    def put(self):

        args = self.parse.parse_args()
        print('qttbelo put args', args)
        res = self.add_updata(args)

        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})

        res_query = QitengRedbookPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengRedbookPrice.query.count()
        res_dict = QitengRedbookPrice.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def delete(self):
        args = self.parse.parse_args()
        print('qttbelo delete args', args)
        qttbelo_obj = QitengRedbookPrice.query.filter(
            QitengRedbookPrice.id == int(args['user_id'])).first()

        if qttbelo_obj:
            try:
                db.session.delete(qttbelo_obj)
                db.session.commit()
            except Exception as e:
                print('e', e)
                return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
        res_query = QitengRedbookPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengRedbookPrice.query.count()
        res_dict = QitengRedbookPrice.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def add_updata(self, args):
        status = args['status']
        if status == 'create':
            rbpoffer = QitengRedbookPrice()
            print('post create')
        else:
            rbpoffer = QitengRedbookPrice.query.filter(
                QitengRedbookPrice.id == int(args['user_id'])).first()
            print('put update', rbpoffer)
        rbpoffer.fans_less = args.get
        rbpoffer.fans_more = args.get
        rbpoffer.offer_less = args.get
        rbpoffer.offer_more = args.get
        rbpoffer.cost_price = args.get
        rbpoffer.brand_partner = args.get

        try:
            rbpoffer.save(rbpoffer)
        except Exception as e:
            db.session.rollback()
            print('TotalResource post except', e)
            return e



# 斗鱼短视频报价
class DouyinShoryViewPrice(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('status', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('fans_less', type=int)
        self.parse.add_argument('fans_more', type=int)
        self.parse.add_argument('star_offer_less', type=float)
        self.parse.add_argument('star_offer_more', type=float)
        self.parse.add_argument('offer_less', type=int)
        self.parse.add_argument('offer_more', type=int)
        self.parse.add_argument('estimated_exposure', type=str)
        self.parse.add_argument('remarks', type=str)

    def get(self):
        args = self.parse.parse_args()
        qttbelo_query = QitengDouyinViewPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengDouyinViewPrice.query.count()
        if qttbelo_query:
            qttbelo_dict = QitengDouyinViewPrice.queryToDict(qttbelo_query)
        else:
            qttbelo_dict = []
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})

    def post(self):

        args = self.parse.parse_args()
        print('qttbelo post args ', args)
        res = self.add_updata(args)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
        else:
            # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            #     int(args['limit'])).all()
            # totle = ResourceTable.query.count()
            # res_dict = ResourceTable.queryToDict(res_query)
            #
            return self.get()

    def put(self):

        args = self.parse.parse_args()
        print('qttbelo put args', args)
        res = self.add_updata(args)

        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})

        res_query = QitengDouyinViewPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengDouyinViewPrice.query.count()
        res_dict = QitengDouyinViewPrice.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def delete(self):
        args = self.parse.parse_args()
        print('qttbelo delete args', args)
        qttbelo_obj = QitengDouyinViewPrice.query.filter(
            QitengDouyinViewPrice.id == int(args['user_id'])).first()

        if qttbelo_obj:
            try:
                db.session.delete(qttbelo_obj)
                db.session.commit()
            except Exception as e:
                print('e', e)
                return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
        res_query = QitengDouyinViewPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
            int(args['limit'])).all()
        totle = QitengDouyinViewPrice.query.count()
        res_dict = QitengDouyinViewPrice.queryToDict(res_query)
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': res_dict}})

    def add_updata(self, args):
        status = args['status']
        if status == 'create':
            tbeloffer = QitengDouyinViewPrice()
            print('post create')
        else:
            tbeloffer = QitengDouyinViewPrice.query.filter(
                QitengDouyinViewPrice.id == int(args['user_id'])).first()
            print('put update', tbeloffer)
        tbeloffer.fans_less = args.get
        tbeloffer.fans_more = args.get
        tbeloffer.star_offer_less = args.get
        tbeloffer.star_offer_more = args.get
        tbeloffer.offer_less = args.get
        tbeloffer.offer_more = args.get
        tbeloffer.estimated_exposure = args.get
        tbeloffer.remarks = args.get

        try:
            tbeloffer.save(tbeloffer)
        except Exception as e:
            db.session.rollback()
            print('TotalResource post except', e)
            return e


ResourceApi.add_resource(TotalResource, '/resourcetable')
ResourceApi.add_resource(TaobaoExportLiveOffer, '/taobaoexportliveprice')
ResourceApi.add_resource(RedbookPrice, '/redbookprice')
ResourceApi.add_resource(DouyinShoryViewPrice, '/douyinshortviewprice')