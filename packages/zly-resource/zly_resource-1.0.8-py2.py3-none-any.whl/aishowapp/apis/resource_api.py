# -*- coding: utf-8 -*-
import json

import requests
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy import and_

from aishowapp.apis.base import BaseAPI
from aishowapp.ext import db

from aishowapp.models.new_resource_model import ResourceTable, QitengDouyinVideoOffer, QitengTaobaoLiveOffer, QitengRedbookPrice, Live, ShortVideo, ImageText, Redbook

ResourceApi = Api(prefix='/platformresource/list')


#达人的增删改查
class TotalResource(Resource,BaseAPI):

    select_dict = {1: '直播淘宝', 2: '直播抖音', 3: '直播快手', 4: '直播苏宁',
                   5: '短视频淘宝', 6: '短视频抖音', 7: '短视频快手', 8: '短视频苏宁',
                   9: '图文淘宝', 10: '图文抖音', 11: '图文快手', 12: '图文苏宁',
                   13: '个性匹配小红书',14:''}

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=str)
        self.parse.add_argument('limit', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('flag', type=str)
        self.parse.add_argument('action', type=str)
        self.parse.add_argument('select_type', type=str)
        self.parse.add_argument('kol_id', type=str)
        self.parse.add_argument('kol_name', type=str)
        self.parse.add_argument('platform', type=str)
        self.parse.add_argument('fans', type=str)
        self.parse.add_argument('cooperation_type', type=str)
        self.parse.add_argument('sex', type=str)
        self.parse.add_argument('status', type=str)
        self.parse.add_argument('hierarchy', type=str)


    def get(self):
        print('resourcetable  get', )
        dic={}
        args = self.parse.parse_args()
        print('resourcetable args',args)
        platform = '' if not args.get('platform') else args.get('platform')
        cooperation_type = '' if not args.get('cooperation_type') else args.get('cooperation_type')
        flag = cooperation_type + platform
        select_type = 14 if not args.get('select_type') else int(args.get('select_type'))
        page = 1 if not args.get('page') else int(args.get('page'))
        limit = 20 if not args.get('limit') else int(args.get('limit'))
        select = self.select_dict.get(select_type,'')

        if select:
            flag = select

        # print('resourcetable flag select_type',select_type)
        # print('resourcetable flag select_type',page,select)
        # print('resourcetable args get',args)
        all_list = []
        totle = 0
        #直播
        if flag.startswith('直播'):
            print('直播')
            live_query = Live.query.offset((page - 1) * limit).limit(limit).all()
            totle = Live.query.count()
            # print('直播222',Live.queryToDict(live_query))
            for item in live_query:
                dict = {}
                dict['live']=Live.queryToDict(item)
                # print('每个直播具体的query对象',dict)
                res_query = item.resource_table

                # print('每个直播对应的resource表的对象res_query',res_query)

                # print('models', res_query.fans)
                # print('models', res_query.total_sell_money)
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                    # print('dict[rsst]', dict['rsst'])
                if  flag.find('淘宝')!=-1:
                    livetaobaoprice_query = QitengTaobaoLiveOffer.query.filter(
                        QitengTaobaoLiveOffer.id == item.qiteng_taobao_live_offer_id).first()
                    if livetaobaoprice_query:
                        dysl_dict = QitengTaobaoLiveOffer.queryToDict(livetaobaoprice_query)
                        # print('直播淘宝对应的价格',dysl_dict)
                        for k, v in dysl_dict.items():
                            if not dict['live'].get(k,None):
                                dict['live'][k] = v
                all_list.append(dict)

        #短视频
        elif  flag.startswith('短视频'):
            print('短视频')
            live_query = ShortVideo.query.offset(( page - 1) * limit).limit(limit).all()
            print(live_query)
            totle = ShortVideo.query.count()
            for item in live_query:
                dict = {}
                dict['video']=ShortVideo.queryToDict(item)
                print(dict['video'])
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                    print(dict['rsst'])
                if flag.find('抖音')!=-1:
                    print(0)
                    videoprice_query = QitengDouyinVideoOffer.query.filter(
                        QitengDouyinVideoOffer.id == item.qiteng_douyin_video_offer_id).first()
                    if videoprice_query:
                        video_dict = QitengDouyinVideoOffer.queryToDict(videoprice_query)
                        for k, v in video_dict.items():
                            if not dict['video'].get(k,None):
                                dict['video'][k] = v
                all_list.append(dict)

        #图文
        elif  flag.startswith('图文'):
            print('图文')
            image_query = ImageText.query.offset(( page - 1) * limit).limit(limit).all()
            totle = ImageText.query.count()
            for item in image_query:
                dict = {}
                dict['image']=ImageText.queryToDict(item)
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                all_list.append(dict)

        #个性匹配
        elif flag.startswith('个性匹配'):

            print('个性匹配')
            live_query = Redbook.query.offset(( page - 1) * limit).limit(limit).all()
            totle = Redbook.query.count()
            for item in live_query:
                dict = {}
                dict['redbook']=Redbook.queryToDict(item)
                print('具体的小红书数据',dict['redbook'])
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                if flag.find('小红书')!=-1:
                    redbook_price_query = QitengRedbookPrice.query.filter(
                        QitengRedbookPrice.id == item.qiteng_redbook_price_id).first()
                    if redbook_price_query:
                        redbook_dict = QitengRedbookPrice.queryToDict(redbook_price_query)
                        print('具体的小红书价格表对应的字典数据',redbook_dict)
                        for k, v in redbook_dict.items():
                            if not dict['redbook'].get(k, None):
                                dict['redbook'][k] = v
                all_list.append(dict)

        print('all_list',json.dumps({'code': 20000, 'data': {'total': totle, 'items': all_list }},ensure_ascii=False))
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': all_list }})

    def post(self):
        print('resource post')
        res = self.add_updata()
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [],'msg':'失败，请输入正确的数据'}})
        else:
            return self.get()

    def put(self):
        print('resource put')
        res = self.add_updata()
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [],'msg':'更新失败，请输入正确的数据'}})
        else:
            return self.get()

    def delete(self):
        args = self.parse.parse_args()
        user_id = None if not args.get('user_id') else int(args.get('user_id'))
        print('resourcetable delete args',args)
        res_query = ResourceTable.query.filter(ResourceTable.id == user_id).first()
        res_id = res_query.id
        print('res_id',res_id)
        platform = args.get('platform')
        cooperation_type = args.get('cooperation_type')
        try:

            if cooperation_type == '直播':  # 抖音专场直播
                print('直播')
                live_query = Live.query.filter(Live.resource_table_id == res_id).first()
                print('live_query',live_query)
                if live_query:
                    db.session.delete(live_query)
                    db.session.flush()
            elif cooperation_type == '短视频':  # 抖音专场直播
                print('短视频')
                svideo_query = ShortVideo.query.filter(ShortVideo.resource_table_id == res_id).first()
                if svideo_query:
                    db.session.delete(svideo_query)
                    db.session.flush()

            elif cooperation_type == '图文':
                print('delete 图文')
                image_query = ImageText.query.filter(ImageText.resource_table_id == res_id).first()
                if image_query:
                    db.session.delete(image_query)
                    db.session.commit()
            elif cooperation_type == '个性匹配':  # 抖音专场直播
                print('个性匹配')
                if platform == '小红书':
                    redbook_query = Redbook.query.filter(Redbook.resource_table_id == res_id).first()
                    if redbook_query:
                        db.session.delete(redbook_query)
                        db.session.flush()
            db.session.delete(res_query)
            db.session.commit()
        except Exception as e:
            print('e', e)
            return e
        return self.get()

    def add_updata(self):
        args = self.parse.parse_args()

        print('资源总表的参数',args)
        action =args['action']

        kol_id = '' if not args.get('kol_id') else args.get('kol_id')
        kol_name = '' if not args.get('kol_name') else args.get('kol_name')
        platform = '' if not args.get('platform') else args.get('platform')
        cooperation_type = '' if not args.get('cooperation_type') else args.get('cooperation_type')
        sex = '男' if not args.get('sex') else args.get('sex')
        status = 0 if not args.get('status') else int(args.get('status'))
        fans = 0 if not args.get('fans') else int(args.get('fans'))
        hierarchy = '' if not args.get('hierarchy') else args.get('hierarchy')
        old_fans = 0
        if action=='create':
            rsourcetab = ResourceTable()
            rsourcetab.kol_id = kol_id
            rsourcetab.kol_name = kol_name
            rsourcetab.platform = platform
            rsourcetab.cooperation_type = cooperation_type
        else :
            rsourcetab = ResourceTable.query.filter(ResourceTable.kol_id==args['kol_id']).first()
            print('updata', rsourcetab)
            old_fans = rsourcetab.fans
        rsourcetab.sex = sex
        rsourcetab.status = status
        rsourcetab.fans = fans
        rsourcetab.hierarchy = hierarchy

        try:

            db.session.add(rsourcetab)
            db.session.flush()

            resource_id =  rsourcetab.id
            print('resource_id',resource_id)
            platform = args.get('platform')
            cooperation_type = args.get('cooperation_type')
            if cooperation_type=='直播':  # 抖音专场直播
                print('进入直播方式')
                self.parse.add_argument('mechanism', type=str)
                self.parse.add_argument('online_number', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('commission', type=str)
                self.parse.add_argument('selection_classification', type=str)
                self.parse.add_argument('avg_viewing_num', type=str)
                self.parse.add_argument('live_time', type=str)
                self.parse.add_argument('introduction', type=str)
                self.parse.add_argument('cooperation_case', type=str)
                self.parse.add_argument('remarks', type=str)

                self.parse.add_argument('single_chain_offer', type=str)
                self.parse.add_argument('single_chain_cost_price', type=str)
                self.parse.add_argument('special_offer', type=str)
                self.parse.add_argument('special_cost_price', type=str)

                args = self.parse.parse_args()
                print('直播方式参数',args)
                mechanism = ''if not args.get('mechanism') else args.get('mechanism')
                export_city = ''if not args.get('export_city') else args.get('export_city')
                commission = ''if not args.get('commission') else args.get('commission')
                selection_classification = ''if not args.get('selection_classification') else args.get('selection_classification')
                introduction = ''if not args.get('introduction') else args.get('introduction')
                cooperation_case = ''if not args.get('cooperation_case') else args.get('cooperation_case')
                remarks = ''if not args.get('remarks') else args.get('remarks')

                online_number= 0 if not args.get('online_number') else int(args.get('online_number'))
                avg_viewing_num= 0 if not args.get('avg_viewing_num') else float(args.get('avg_viewing_num'))
                live_time= 0 if not args.get('live_time') else float(args.get('live_time'))
                single_chain_offer= 0 if not args.get('single_chain_offer') else int(args.get('single_chain_offer'))
                single_chain_cost_price= 0 if not args.get('single_chain_cost_price') else int(args.get('single_chain_cost_price'))
                special_offer= 0 if not args.get('special_offer') else int(args.get('special_offer'))
                special_cost_price= 0 if not args.get('special_cost_price') else int(args.get('special_cost_price'))

                # 判断是不是更新还是创建

                print('action',action)
                if action == 'create':
                    qtlive = Live()
                    qtlive.resource_table_id = resource_id
                else:
                    qtlive = Live.query.filter(Live.resource_table_id==resource_id).first()
                qtlive.mechanism = mechanism
                qtlive.export_city = export_city
                qtlive.commission = commission
                qtlive.selection_classification = selection_classification
                qtlive.introduction = introduction
                qtlive.cooperation_case = cooperation_case
                qtlive.remarks = remarks
                qtlive.online_number = online_number
                qtlive.live_time = live_time

                # 判断具体是那个直播表，若是淘宝则批量，否则手动添加
                print('platform', platform)
                if platform =='淘宝':
                    #判断是不是更新还有场均观看人数是否改变，若改变则批量更新，若没变则单个更新
                    if action=='create' or qtlive.avg_viewing_num != avg_viewing_num:
                        qtdvp = QitengTaobaoLiveOffer.query.filter(and_(QitengTaobaoLiveOffer.avg_viewing_num_less < avg_viewing_num,
                                                                        QitengTaobaoLiveOffer.avg_viewing_num_more >=avg_viewing_num)).first()
                        print('淘宝 qtdvp',qtdvp)
                        if qtdvp:
                            qtlive.qiteng_taobao_live_offer_id = qtdvp.id
                            qtlive.avg_viewing_num = avg_viewing_num
                            qtlive.single_chain_offer = qtdvp.single_chain_offer
                            qtlive.single_chain_cost_price = qtdvp.single_chain_cost_price
                            qtlive.special_offer = qtdvp.special_offer
                            qtlive.special_cost_price = qtdvp.special_cost_price
                    else :
                        qtlive.avg_viewing_num = avg_viewing_num
                        qtlive.single_chain_offer = single_chain_offer
                        qtlive.single_chain_cost_price = single_chain_cost_price
                        qtlive.special_offer = special_offer
                        qtlive.special_cost_price = special_cost_price
                else:
                    # print('更新或者创建非淘宝的订单',)
                    # print('single_chain_offer',single_chain_offer)
                    # print('single_chain_cost_price',single_chain_cost_price)
                    # print('special_offer',special_offer)
                    # print('special_cost_price',special_cost_price)
                    qtlive.avg_viewing_num = avg_viewing_num
                    qtlive.single_chain_offer = single_chain_offer
                    qtlive.single_chain_cost_price = single_chain_cost_price
                    qtlive.special_offer = special_offer
                    qtlive.special_cost_price = special_cost_price

                db.session.add(qtlive)
                db.session.flush()
                res = Live.query.all()
                print('res',Live.queryToDict(res))
            elif cooperation_type == '短视频':  # 抖音专场直播
                print('短视频')
                self.parse.add_argument('dianzan', type=str)
                self.parse.add_argument('export_home_page', type=str)
                self.parse.add_argument('export_tag', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('offer_0_20s', type=str)
                self.parse.add_argument('cost_0_20s', type=str)
                self.parse.add_argument('offer_21_60s', type=str)
                self.parse.add_argument('cost_21_60s', type=str)
                self.parse.add_argument('introduction', type=str)
                self.parse.add_argument('cooperation_case', type=str)
                self.parse.add_argument('remarks', type=str)
                args = self.parse.parse_args()

                dianzan = 0 if not args.get('dianzan') else float(args.get('dianzan'))
                export_home_page = '' if not args.get('export_home_page') else args.get('export_home_page')
                export_tag = '' if not args.get('export_tag') else args.get('export_tag')
                export_city = '' if not args.get('export_city') else args.get('export_city')
                offer_0_20s = 0 if not args.get('offer_0_20s') else int(args.get('offer_0_20s'))
                cost_0_20s = 0 if not args.get('cost_0_20s') else int(args.get('cost_0_20s'))
                cost_21_60s = 0 if not args.get('cost_21_60s') else int(args.get('cost_21_60s'))
                offer_21_60s = 0 if not args.get('offer_21_60s') else int(args.get('offer_21_60s'))
                introduction = '' if not args.get('introduction') else args.get('introduction')
                cooperation_case = '' if not args.get('cooperation_case') else args.get('cooperation_case')
                remarks = '' if not args.get('introduction') else args.get('remarks')

                # 判断是不是更新还是创建
                if action == 'create':
                    qtvideo = ShortVideo()
                    qtvideo.resource_table_id = resource_id

                else:
                    qtvideo = ShortVideo.query.filter(ShortVideo.resource_table_id == resource_id).first()

                qtvideo.dianzan = dianzan
                qtvideo.export_home_page = export_home_page
                qtvideo.export_tag = export_tag
                qtvideo.export_city = export_city
                qtvideo.introduction = introduction
                qtvideo.cooperation_case = cooperation_case
                qtvideo.remarks = remarks

                # 判断具体是那个直播表，若是淘宝则批量，否则手动添加
                if platform == '抖音':
                    # 判断是不是更新还有fans人数是否改变，若改变则批量更新，若没变则单个更新
                    if action == 'create' or old_fans != fans:
                        qtdyvideooffer = QitengDouyinVideoOffer.query.filter(
                            and_(QitengDouyinVideoOffer.fans_less < fans,
                                 QitengDouyinVideoOffer.fans_more >= fans)).first()
                        if qtdyvideooffer:
                            qtvideo.qiteng_douyin_video_offer_id=qtdyvideooffer.id
                            qtvideo.cost_0_20s = qtdyvideooffer.cost_0_20s
                            qtvideo.offer_0_20s = qtdyvideooffer.offer_0_20s
                            qtvideo.cost_21_60s = qtdyvideooffer.cost_21_60s
                            qtvideo.offer_21_60s = qtdyvideooffer.offer_21_60s
                    else:
                        qtvideo.cost_0_20s = cost_0_20s
                        qtvideo.offer_0_20s = offer_0_20s
                        qtvideo.cost_21_60s = cost_21_60s
                        qtvideo.offer_21_60s = offer_21_60s
                else:
                    qtvideo.cost_0_20s = cost_0_20s
                    qtvideo.offer_0_20s = offer_0_20s
                    qtvideo.cost_21_60s = cost_21_60s
                    qtvideo.offer_21_60s = offer_21_60s

                db.session.add(qtvideo)
                db.session.flush()

            elif cooperation_type == '图文':  # 抖音专场直播

                print('图文')
                self.parse.add_argument('mechanism', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('export_classification', type=str)
                self.parse.add_argument('image_cost_price', type=int)
                self.parse.add_argument('image_offer', type=str)
                self.parse.add_argument('channel_interpretation', type=str)
                self.parse.add_argument('remarks', type=str)

                args = self.parse.parse_args()

                mechanism = '' if not args.get('mechanism') else args.get('mechanism')
                export_classification = '' if not args.get('export_classification') else args.get('export_classification')
                export_tag = '' if not args.get('export_tag') else args.get('export_tag')
                image_cost_price = 0 if not args.get('image_cost_price') else int(args.get('image_cost_price'))
                image_offer = 0 if not args.get('image_offer') else int(args.get('image_offer'))
                channel_interpretation = '' if not args.get('channel_interpretation') else args.get('channel_interpretation')
                remarks = '' if not args.get('remarks') else args.get('remarks')

                # 判断是不是更新还是创建
                if action == 'create':
                    qtimage = ImageText()
                    qtimage.resource_table_id = resource_id

                else:
                    qtimage = ImageText.query.filter(ImageText.resource_table_id == resource_id).first()

                qtimage.mechanism = mechanism
                qtimage.export_tag = export_tag
                qtimage.export_classification = export_classification
                qtimage.image_cost_price = image_cost_price
                qtimage.image_offer = image_offer
                qtimage.channel_interpretation = channel_interpretation
                qtimage.remarks = remarks

                db.session.add(qtimage)
                db.session.flush()

            elif cooperation_type == '个性匹配':
                self.parse.add_argument('export_home_page', type=str)
                self.parse.add_argument('dianzan', type=str)
                self.parse.add_argument('export_city', type=str)
                self.parse.add_argument('export_tag', type=str)
                self.parse.add_argument('cost_price_image_text', type=str)
                self.parse.add_argument('offer_image_text', type=str)
                self.parse.add_argument('red_book_cost_price_video', type=str)
                self.parse.add_argument('red_book_offer_video', type=str)
                self.parse.add_argument('brand_partner', type=str)
                self.parse.add_argument('cooperation_case', type=str)
                self.parse.add_argument('remarks', type=str)

                args = self.parse.parse_args()

                export_home_page = '' if not args.get('export_home_page') else args.get('export_home_page')
                dianzan = 0 if not args.get('dianzan') else int(args.get('dianzan'))
                export_city = '' if not args.get('export_city') else args.get('export_city')
                export_tag = '' if not args.get('export_tag') else args.get('export_tag')
                cost_price_image_text = 0 if not args.get('cost_price_image_text') else int(args.get('cost_price_image_text'))
                offer_image_text = 0 if not args.get('offer_image_text') else int(args.get('offer_image_text'))
                red_book_cost_price_video = 0 if not args.get('red_book_cost_price_video') else int(args.get('red_book_cost_price_video'))
                red_book_offer_video = 0 if not args.get('red_book_offer_video') else int(args.get('red_book_offer_video'))
                brand_partner = True if  args.get('brand_partner')=='true' else False
                cooperation_case = '' if not args.get('cooperation_case') else args.get('cooperation_case')
                remarks = '' if not args.get('remarks') else args.get('remarks')

                print('小红书',args)
                if action == 'create':
                    print('小红书创建')
                    redbook = Redbook()
                    redbook.resource_table_id = resource_id
                else:
                    print('小红书更新')
                    redbook = Redbook.query.filter(Redbook.resource_table_id==resource_id).first()

                redbook.export_home_page =export_home_page
                redbook.dianzan = dianzan
                redbook.export_city = export_city
                redbook.export_tag = export_tag
                redbook.brand_partner = brand_partner
                redbook.cooperation_case = cooperation_case
                redbook.remarks = remarks

                # 判断具体是那个直播表，若是淘宝则批量，否则手动添加
                if platform =='小红书':

                    # 判断是不是更新还有fans人数是否改变，若改变则批量更新，若没变则单个更新
                    qtredbookp = QitengRedbookPrice.query.filter(
                        and_(QitengRedbookPrice.fans_less < fans,
                             QitengRedbookPrice.fans_more >= fans)).first()
                    print('小红书对应的价格对象',QitengRedbookPrice.queryToDict(qtredbookp))
                    print('当前操作',action)
                    print('粉丝数',fans)
                    print('旧粉丝数',old_fans)
                    if action == 'create' or old_fans != fans:
                        print('小红书批量更改价格')
                        if qtredbookp:
                            if redbook.brand_partner:
                                redbook.qiteng_redbook_price_id = qtredbookp.id
                                redbook.offer_image_text = qtredbookp.brand_image_offer
                                redbook.cost_price_image_text = qtredbookp.brand_image_cost_price
                                redbook.red_book_offer_video = qtredbookp.brand_video_offer
                                redbook.red_book_cost_price_video = qtredbookp.brand_viedo_cost_price
                            else:
                                redbook.qiteng_redbook_price_id = qtredbookp.id
                                redbook.offer_image_text = qtredbookp.image_offer
                                redbook.cost_price_image_text = qtredbookp.image_cost_price
                                redbook.red_book_offer_video = qtredbookp.video_offer
                                redbook.red_book_cost_price_video = qtredbookp.viedo_cost_price
                    else:
                        print('当修改的是具体的价格')
                        print('offer_image_text',offer_image_text)
                        print('cost_price_image_text',cost_price_image_text)
                        print('red_book_offer_video',red_book_offer_video)
                        print('red_book_cost_price_video',red_book_cost_price_video)
                        redbook.offer_image_text = offer_image_text
                        redbook.cost_price_image_text = cost_price_image_text
                        redbook.red_book_offer_video = red_book_offer_video
                        redbook.red_book_cost_price_video = red_book_cost_price_video
                else:
                    print('不是小红书')
                    redbook.image_offer = offer_image_text
                    redbook.image_cost_price = cost_price_image_text
                    redbook.video_offer = red_book_offer_video
                    redbook.viedo_cost_price = red_book_cost_price_video

                db.session.add(redbook)
                db.session.flush()

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('TotalResource post except', e)
            return e

    def resource_get_list(self,select_type,page,limit):
        """
        资源

        :param page: 页码
        :param limit: 标签数量
        :return:
        """
        # # res = requests.get(
        # #     "https://oapi.dingtalk.com/user/getuserinfo?access_token=" + "eddded8cef963e4e92ffcf62d3dd158a" + "&code=" + code)
        # import json
        # headers = {'Content-Type': 'application/json'}

        # response = requests.get("http://47.110.58.200:8081/api/v1.0/platformresource/list/resourcetable?select_type=1&page=1&limit=20")

        # print("start", response)
        response = self._get('/platformresource/list/resourcetable',params={'select_type':select_type,'page':page,'limit':limit})

        return response

#麒腾淘宝KOL直播报价
# class TaobaoExportLiveOffer(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#         self.parse.add_argument('status', type=str)
#         self.parse.add_argument('user_id', type=str)
#         self.parse.add_argument('hierarchy', type=str)
#         self.parse.add_argument('avg_viewing_num_less', type=float)
#         self.parse.add_argument('avg_viewing_num_more', type=float)
#         self.parse.add_argument('offer_less', type=int)
#         self.parse.add_argument('offer_more', type=int)
#         self.parse.add_argument('cost_price', type=str)
#         self.parse.add_argument('remarks', type=str)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('qttbelo get args ', args)
#         qttbelo_query = QitengTaobaoExportLiveOffer.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#             int(args['limit'])).all()
#         totle = QitengTaobaoExportLiveOffer.query.count()
#         if qttbelo_query:
#             qttbelo_dict = QitengTaobaoExportLiveOffer.queryToDict(qttbelo_query)
#         else:
#             qttbelo_dict=[]
#         return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})
#
#
#     def post(self):
#
#         args = self.parse.parse_args()
#         print('qttbelo post args ', args)
#         res = self.add_updata(args)
#
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '创建失败，请输入正确的数据'}})
#         else:
#             # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#             #     int(args['limit'])).all()
#             # totle = ResourceTable.query.count()
#             # res_dict = ResourceTable.queryToDict(res_query)
#             #
#             return self.get()
#
#
#     def put(self):
#
#         args = self.parse.parse_args()
#         print('qttbelo put args',args)
#         res = self.add_updata(args)
#
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})
#         return self.get()
#
#     def delete(self):
#
#         args = self.parse.parse_args()
#         print('qttbelo delete args', args)
#         qttbelo_obj = QitengTaobaoExportLiveOffer.query.filter(QitengTaobaoExportLiveOffer.id == int(args['user_id'])).first()
#
#         if qttbelo_obj:
#             #修改淘宝直播表的值
#             for item in qttbelo_obj.taobao_lives:
#                 item.taobao_offer = 0
#                 item.taobao_cost_price = 0
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('TaobaoLive save fail', e)
#                     return e
#             try:
#                 db.session.delete(qttbelo_obj)
#                 db.session.commit()
#             except Exception as e:
#                 print('e', e)
#                 return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
#         # res_query = QitengTaobaoExportLiveOffer.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#         #     int(args['limit'])).all()
#         # totle = QitengTaobaoExportLiveOffer.query.count()
#         # res_dict = QitengTaobaoExportLiveOffer.queryToDict(res_query)
#         return self.get()
#
#     def add_updata(self, args):
#
#         status = args['status']
#         if status == 'create':
#             tbeloffer = QitengTaobaoExportLiveOffer()
#             print('post create')
#         else:
#             tbeloffer = QitengTaobaoExportLiveOffer.query.filter(QitengTaobaoExportLiveOffer.id == int(args['user_id'])).first()
#             print('put update',tbeloffer)
#         tbeloffer.hierarchy = args.get
#         tbeloffer.avg_viewing_num_less = args.get
#         tbeloffer.avg_viewing_num_more = args.get
#         tbeloffer.offer_less = args.get
#         tbeloffer.offer_more = args.get
#         tbeloffer.cost_price = args.get
#         tbeloffer.remarks = args.get
#         if status == 'update':
#             # 修改淘宝直播表的值
#             for item in tbeloffer.taobao_lives:
#                 item.taobao_offer = args.get
#                 item.taobao_cost_price = args.get
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('TaobaoLive save fail', e)
#                     return e
#         try:
#             tbeloffer.save(tbeloffer)
#         except Exception as e:
#             db.session.rollback()
#             print('TotalResource post except', e)
#             return e


# 小红书报价
# class RedbookPrice(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#         self.parse.add_argument('status', type=str)
#         self.parse.add_argument('user_id', type=str)
#         self.parse.add_argument('fans_less', type=float)
#         self.parse.add_argument('fans_more', type=float)
#         self.parse.add_argument('cost_price', type=int)
#         self.parse.add_argument('brand_partner_cost_price', type=int)
#         self.parse.add_argument('offer_less', type=int)
#         self.parse.add_argument('offer_more', type=int)
#         self.parse.add_argument('brand_partner_offer_less', type=int)
#         self.parse.add_argument('brand_partner_offer_more', type=int)
#         self.parse.add_argument('remarks', type=str)
#         self.parse.add_argument('brand_partner_remarks', type=str)
#         self.parse.add_argument('brand_partner', type=bool)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('qttbelo post args ', args)
#         qttbelo_query = QitengRedbookPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#             int(args['limit'])).all()
#         totle = QitengRedbookPrice.query.count()
#         if qttbelo_query:
#             qttbelo_dict = QitengRedbookPrice.queryToDict(qttbelo_query)
#         else:
#             qttbelo_dict = []
#         return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})
#
#     def post(self):
#
#         args = self.parse.parse_args()
#         print('qtrebbookp post args ', args)
#         res = self.add_updata(args)
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
#         else:
#             return self.get()
#
#     def put(self):
#
#         args = self.parse.parse_args()
#         print('qtrebbookp put args', args)
#         res = self.add_updata(args)
#
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})
#
#         return self.get()
#
#     def delete(self):
#         args = self.parse.parse_args()
#         print('qtrebbookp delete args', args)
#         qtrdp_obj = QitengRedbookPrice.query.filter(
#             QitengRedbookPrice.id == int(args['user_id'])).first()
#         if qtrdp_obj:
#             #修改小红书的值
#             for item in qtrdp_obj.redbook_image_text_links:
#                 item.redbook_offer = 0
#                 item.redbook_cost_price = 0
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('Redbook save fail', e)
#                     return e
#             try:
#                 db.session.delete(qtrdp_obj)
#                 db.session.commit()
#             except Exception as e:
#                 print('e', e)
#                 return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
#         return self.get()
#
#     def add_updata(self, args):
#         status = args['status']
#         if status == 'create':
#             rbpoffer = QitengRedbookPrice()
#             print('post create')
#         else:
#             rbpoffer = QitengRedbookPrice.query.filter(
#                 QitengRedbookPrice.id == int(args['user_id'])).first()
#             print('put update', rbpoffer)
#         rbpoffer.fans_less = args.get
#         rbpoffer.fans_more = args.get
#         rbpoffer.offer_less = args.get
#         rbpoffer.offer_more = args.get
#         rbpoffer.brand_partner_offer_less = args.get
#         rbpoffer.brand_partner_offer_more = args.get
#         rbpoffer.cost_price = args.get
#         rbpoffer.brand_partner_cost_price = args.get
#         rbpoffer.remarks = args.get
#         rbpoffer.brand_partner_remarks = args.get
#         rbpoffer.brand_partner = args.get
#
#         if status == 'update':
#             # 修改小红书图文链接的值
#             print('修改小红书图文链接的值')
#             print('修改小红书图文链接的值',rbpoffer.redbook_image_text_links)
#             for item in rbpoffer.redbook_image_text_links:
#                 print('小红书对应的图文连接的query对象',item)
#                 if item.brand_partner:
#                     item.redbook_offer = args.get
#                     item.redbook_cost_price = args.get
#                 else:
#                     item.redbook_offer = args.get
#                     item.redbook_cost_price = args.get
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('RedbookImageTextLink save fail', e)
#                     return e
#         try:
#             rbpoffer.save(rbpoffer)
#         except Exception as e:
#             db.session.rollback()
#             print('QitengRedbookPrice post except', e)
#             return e


# 抖音短视频报价
# class DouyinShoryViewPrice(Resource):
#
#     def __init__(self):
#         self.parse = reqparse.RequestParser()
#         self.parse.add_argument('page', type=int)
#         self.parse.add_argument('limit', type=int)
#         self.parse.add_argument('status', type=str)
#         self.parse.add_argument('user_id', type=str)
#         self.parse.add_argument('fans_less', type=int)
#         self.parse.add_argument('fans_more', type=int)
#         self.parse.add_argument('star_offer_less', type=float)
#         self.parse.add_argument('star_offer_more', type=float)
#         self.parse.add_argument('offer_less', type=int)
#         self.parse.add_argument('offer_more', type=int)
#         self.parse.add_argument('cost_price', type=int)
#         self.parse.add_argument('estimated_exposure', type=str)
#         self.parse.add_argument('remarks', type=str)
#
#     def get(self):
#         args = self.parse.parse_args()
#         print('DouyinShoryViewPrice get args', args)
#         qttbelo_query = QitengDouyinViewPrice.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#             int(args['limit'])).all()
#         totle = QitengDouyinViewPrice.query.count()
#         if qttbelo_query:
#             qttbelo_dict = QitengDouyinViewPrice.queryToDict(qttbelo_query)
#         else:
#             qttbelo_dict = []
#         return jsonify({'code': 20000, 'data': {'total': totle, 'items': qttbelo_dict}})
#
#     def post(self):
#
#         args = self.parse.parse_args()
#         print('DouyinShoryViewPrice post args ', args)
#         res = self.add_updata(args)
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
#         else:
#             # res_query = ResourceTable.query.offset((int(args['page']) - 1) * int(args['limit'])).limit(
#             #     int(args['limit'])).all()
#             # totle = ResourceTable.query.count()
#             # res_dict = ResourceTable.queryToDict(res_query)
#             #
#             return self.get()
#
#     def put(self):
#
#         args = self.parse.parse_args()
#         print('DouyinShoryViewPrice put args', args)
#         res = self.add_updata(args)
#
#         if res:
#             return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})
#
#         return self.get()
#
#     def delete(self):
#         args = self.parse.parse_args()
#         print('DouyinShoryViewPrice delete args', args)
#         qttbelo_obj = QitengDouyinViewPrice.query.filter(
#             QitengDouyinViewPrice.id == int(args['user_id'])).first()
#
#         if qttbelo_obj:
#             # 处理抖音短视频的报价字段和成本价
#             for item in qttbelo_obj.douyin_view_exports:
#                 item.star_offer = 0
#                 item.offer_more = 0
#                 item.offer_less = 0
#                 item.douyin_view_cost_price = 0
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('DouyinShoryView save fail', e)
#                     return e
#             try:
#                 db.session.delete(qttbelo_obj)
#                 db.session.commit()
#             except Exception as e:
#                 print('e', e)
#                 return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '，请重新选择数据'}})
#         return self.get()
#
#     def add_updata(self, args):
#         status = args['status']
#         if status == 'create':
#             tbeloffer = QitengDouyinViewPrice()
#             print('post create')
#         else:
#             tbeloffer = QitengDouyinViewPrice.query.filter(
#                 QitengDouyinViewPrice.id == int(args['user_id'])).first()
#             print('put update', tbeloffer)
#         tbeloffer.fans_less = args.get
#         tbeloffer.fans_more = args.get
#         tbeloffer.star_offer_less = args.get
#         tbeloffer.star_offer_more = args.get
#         tbeloffer.offer_less = args.get
#         tbeloffer.offer_more = args.get
#         tbeloffer.estimated_exposure = args.get
#         tbeloffer.cost_price = args.get
#         tbeloffer.remarks = args.get
#
#         if status == 'update':
#             # #处理抖音短视频的报价字段和成本价
#             for item in tbeloffer.douyin_view_exports:
#                 print("找到每一个短视频的query对象",item)
#                 item.star_offer = args.get
#                 item.offer_more = args.get
#                 item.offer_less = args.get
#                 item.douyin_view_cost_price = args.get
#                 try:
#                     item.save(item)
#                 except Exception as e:
#                     db.session.rollback()
#                     print('TaobaoLive save fail', e)
#                     return e
#         try:
#             tbeloffer.save(tbeloffer)
#         except Exception as e:
#             db.session.rollback()
#             print('TotalResource post except',e)
#             return e

class PriceResource(Resource):
    select_dict = {1: '直播淘宝', 2: '直播抖音', 3: '直播快手', 4: '直播苏宁',
                   5: '短视频淘宝', 6: '短视频抖音', 7: '短视频快手', 8: '短视频苏宁',
                   9: '图文淘宝', 10: '图文抖音', 11: '图文快手', 12: '图文苏宁',
                   13: '个性匹配小红书', 14: ''}

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=int)
        self.parse.add_argument('limit', type=int)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('status', type=str)
        self.parse.add_argument('live_name', type=str)
        self.parse.add_argument('select_type', type=str)

    def get(self):
        print('resource_price get')
        args = self.parse.parse_args()
        print(args)
        live_name = '直播淘宝' if not args.get('live_name') else args.get('live_name')
        select_type = 14 if not args.get('select_type') else args.get('select_type')
        page = 1 if not args.get('select_type') else args.get('select_type')
        limit = 20 if not args.get('select_type') else args.get('select_type')
        select = self.select_dict[select_type]
        if select:
            live_name = select
        totle=0
        all_list=[]
        if live_name=='直播淘宝' :
            live_query = QitengTaobaoLiveOffer.query.offset((page - 1) * limit).limit(limit).all()
            totle = QitengTaobaoLiveOffer.query.count()
            if live_query:
                all_list=QitengTaobaoLiveOffer.queryToDict(live_query)
        elif live_name == '短视频抖音' :
            live_query = QitengDouyinVideoOffer.query.offset((page - 1) * limit).limit(limit).all()
            totle = QitengDouyinVideoOffer.query.count()
            if live_query:
                print(111)
                all_list=QitengDouyinVideoOffer.queryToDict(live_query)
                print(all_list)

        elif live_name == '个性匹配小红书':
            live_query = QitengRedbookPrice.query.offset((args['page'] - 1) * args['limit']).limit(
                args['limit']).all()
            totle = QitengRedbookPrice.query.count()
            totle = totle
            if live_query:
                all_list=QitengRedbookPrice.queryToDict(live_query)
        print('all_list', json.dumps({'code': 20000, 'data': {'total': totle, 'items': all_list}}, ensure_ascii=False))
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': all_list}})

    def post(self):
        print('resource_price post')
        res = self.add_updata()
        print('resource_price post res', res)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '失败，请输入正确的数据'}})
        else:
            return self.get()

    def put(self):
        print('resource_price put')

        res = self.add_updata()
        print('resource_price put res', res)
        if res:
            return jsonify({'code': 20000, 'data': {'total': 0, 'items': [], 'msg': '更新失败，请输入正确的数据'}})
        else:
            return self.get()

    def delete(self):
        print('resource_price delete')
        args = self.parse.parse_args()
        print('resource_price delete args',args)
        live_name = '直播淘宝' if not  args.get('live_name') else args.get('live_name')
        user_id = args.get('user_id')
        status = args.get('status')
        if live_name.startswith('直播'):
            print(0)
            qtlive = None
            if status == 'delete':
                # 判断当是创建时的直播表
                if live_name.find('淘宝')!=-1:
                    qtlive=QitengTaobaoLiveOffer.query.filter(QitengTaobaoLiveOffer.id == user_id).first()
                    print(1)
                elif live_name.find('抖音')!=-1:
                    pass
                elif live_name.find('快手')!=-1:
                    pass
                elif live_name.find('苏宁')!=-1:
                    pass
            if qtlive:
                for item in qtlive.lives:
                    item.single_chain_offer = 0
                    item.single_cost_price = 0
                    item.special_offer = 0
                    item.special_cost_price = 0
                    try:
                        item.save(item)
                    except Exception as e:
                        print('Lives save fail', e)
                        return e
            try:
                db.session.delete(qtlive)
                db.session.commit()
            except Exception as e:
                print('QitengTaobaoLiveOffer save fail', e)
                return e
        elif live_name.startswith('短视频'):
            qtview = None
            if status == 'delete':
                # 判断当是删除的短视频表
                if live_name.find('淘宝') != -1:
                    pass
                elif live_name.find('抖音') != -1:
                    qtview = QitengDouyinVideoOffer.query.filter(QitengDouyinVideoOffer.id == user_id).first()
                elif live_name.find('快手') != -1:
                    pass
                elif live_name.find('苏宁') != -1:
                    pass
            if qtview:
                for item in qtview.short_videos:
                    item.cost_0_20s = 0
                    item.offer_0_20s = 0
                    item.cost_21_60s = 0
                    item.offer_21_60s = 0
                    try:
                        item.save(item)
                    except Exception as e:
                        print('Lives save fail', e)
                        return e
            try:
                db.session.delete(qtview)
                db.session.commit()
            except Exception as e:
                print('QitengTaobaoLiveOffer save fail', e)
                return e
        elif live_name.startswith('图文') :
            qtimage = None
            if status == 'delete':
                # 判断当是创建时的图文表
                if live_name.find('淘宝') != -1:
                    pass
                elif live_name.find('京东') != -1:
                    pass
                elif live_name.find('抖音') != -1:
                    pass
                elif live_name.find('快手') != -1:
                    pass
                elif live_name.find('苏宁') != -1:
                    pass
            if qtimage:
                for item in qtimage.image_texts:
                    item.image_text_offer = 0
                    item.image_text_cost_price = 0
                    try:
                        item.save(item)
                    except Exception as e:
                        print('Lives save fail', e)
                        return e
            try:

                db.session.delete(qtimage)
                db.session.commit()
            except Exception as e:
                print('QitengTaobaoLiveOffer save fail', e)
                return e
        elif live_name.startswith('个性匹配') :
            qtmatchredbook = None
            if status == 'delete':
                # 判断当是创建时的直播表
                if live_name.find('小红书') != -1:
                    qtmatchredbook = QitengRedbookPrice.query.filter(
                        QitengRedbookPrice.id == user_id).first()
                elif live_name.find('淘宝') != -1:
                    pass
                elif live_name.find('抖音') != -1:
                    pass
                elif live_name.find('快手') != -1:
                    pass
                elif live_name.find('苏宁') != -1:
                    pass
            if qtmatchredbook:
                for item in qtmatchredbook.redbooks:
                    item.offer_image_text = 0
                    item.cost_price_image_text = 0
                    item.red_book_offer_video = 0
                    item.red_book_cost_price_video = 0
                    try:
                        item.save(item)
                    except Exception as e:
                        print('Lives save fail', e)
                        return e
            try:
                db.session.delete(qtmatchredbook)
                db.session.commit()
            except Exception as e:
                print('QitengTaobaoLiveOffer save fail', e)
                return e

        return self.get()

    def add_updata(self):
        args = self.parse.parse_args()
        action = args.get('status')
        user_id = args.get('user_id')
        live_name = args.get('live_name')
        print('args',args)
        print('live_name',live_name)
        if live_name == '直播淘宝':
            self.parse.add_argument('hierarchy', type=str)
            self.parse.add_argument('avg_viewing_num_less', type=float)
            self.parse.add_argument('avg_viewing_num_more', type=float)
            self.parse.add_argument('single_chain_offer', type=int)
            self.parse.add_argument('single_chain_cost_price', type=int)
            self.parse.add_argument('special_offer', type=int)
            self.parse.add_argument('special_cost_price', type=int)
            self.parse.add_argument('remarks', type=str)

            args = self.parse.parse_args()
            print('直播淘宝',args)
            # 判断是不是创建
            if action == 'create':
                qtlive=QitengTaobaoLiveOffer()
                print(qtlive)
            else:
                qtlive = QitengTaobaoLiveOffer.query.filter(QitengTaobaoLiveOffer.id == user_id).first()

            if qtlive:
                qtlive.hierarchy=args.get('hierarchy')
                qtlive.avg_viewing_num_less=0 if not args.get('avg_viewing_num_less') else args.get('avg_viewing_num_less')
                qtlive.avg_viewing_num_more=0 if not args.get('avg_viewing_num_more') else args.get('avg_viewing_num_more')
                qtlive.single_chain_offer=0 if not args.get('single_chain_offer') else args.get('single_chain_offer')
                qtlive.single_chain_cost_price=0 if not args.get('single_chain_cost_price') else args.get('single_chain_cost_price')
                qtlive.special_offer=0 if not args.get('special_offer') else args.get('special_offer')
                qtlive.special_cost_price=0 if not args.get('special_cost_price') else args.get('special_cost_price')
                qtlive.remarks=args.get('remarks')
                if action == 'update':
                    print('update')
                    for item in qtlive.lives:
                        if item:
                            item.single_chain_offer = 0 if not args.get('single_chain_offer') else args.get('single_chain_offer')
                            item.single_cost_price = 0 if not args.get('single_cost_price') else args.get('single_cost_price')
                            item.special_offer = 0 if not args.get('special_offer') else args.get('special_offer')
                            item.special_cost_price = 0 if not args.get('special_cost_price') else args.get('special_cost_price')

                            try:
                                item.save(item)
                            except Exception as e:
                                print('Lives save fail', e)
                                return e
            try:
                qtlive.save(qtlive)
            except Exception as e:
                print('QitengTaobaoLiveOffer save fail',e)
                return e
        elif live_name=='短视频抖音':

            self.parse.add_argument('fans_less', type=float)
            self.parse.add_argument('fans_more', type=float)
            self.parse.add_argument('offer_0_20s', type=int)
            self.parse.add_argument('cost_0_20s', type=int)
            self.parse.add_argument('offer_21_60s', type=int)
            self.parse.add_argument('cost_21_60s', type=int)
            self.parse.add_argument('star_offer_0_20s', type=int)
            self.parse.add_argument('star_offer_21_60s', type=int)
            self.parse.add_argument('estimated_0_20s', type=float)
            self.parse.add_argument('estimated_21_60s', type=float)
            self.parse.add_argument('remarks', type=str)

            args = self.parse.parse_args()

            # 判断是不是创建
            if action == 'create':
                qtview = QitengDouyinVideoOffer()
            # 判断是不是更新
            else:
                qtview = QitengDouyinVideoOffer.query.filter(QitengDouyinVideoOffer.id == user_id).first()
            qtview.hierarchy = args.get('hierarchy')
            qtview.fans_less = 0 if not args.get('fans_less') else args.get('fans_less')
            qtview.fans_more = 0 if not args.get('fans_more') else args.get('fans_more')
            qtview.cost_0_20s = 0 if not args.get('cost_0_20s') else args.get('cost_0_20s')
            qtview.offer_0_20s = 0 if not args.get('offer_0_20s') else args.get('offer_0_20s')
            qtview.cost_21_60s = 0 if not args.get('cost_21_60s') else args.get('cost_21_60s')
            qtview.offer_21_60s = 0 if not args.get('offer_21_60s') else args.get('offer_21_60s')
            qtview.star_offer_0_20s = 0 if not args.get('star_offer_0_20s') else args.get('star_offer_0_20s')
            qtview.star_offer_21_60s = 0 if not args.get('star_offer_21_60s') else args.get('star_offer_21_60s')
            qtview.estimated_0_20s = 0 if not args.get('estimated_0_20s') else args.get('estimated_0_20s')
            qtview.estimated_21_60s = 0 if not args.get('estimated_21_60s') else args.get('estimated_21_60s')
            qtview.remarks = '' if not args.get('remarks') else args.get('remarks')

            if action == 'update':
                for item in qtview.short_videos:
                    if item:
                        item.cost_0_20s =  0 if not args.get('cost_0_20s') else args.get('cost_0_20s')
                        item.offer_0_20s = 0 if not args.get('offer_0_20s') else args.get('offer_0_20s')
                        item.cost_21_60s = 0 if not args.get('cost_21_60s') else args.get('cost_21_60s')
                        item.offer_21_60s = 0 if not args.get('offer_21_60s') else args.get('offer_21_60s')
                        try:
                            item.save(item)
                        except Exception as e:
                            print('View save fail', e)
                            return e
            try:
                qtview.save(qtview)
            except Exception as e:
                print('QitenViewOffer save fail', e)
                return e
        # elif live_name.startswith('图文'):
        #         self.parse.add_argument('fans_less', type=str)
        #         self.parse.add_argument('fans_more', type=str)
        #         self.parse.add_argument('image_text_offer', type=str)
        #         self.parse.add_argument('image_text_cost_price', type=str)
        #         self.parse.add_argument('remarks', type=str)
        #         args = self.parse.parse_args()
        #         # 判断是不是创建
        #         qtimage = None
        #         if status == 'create':
        #             # 判断当是创建时的图文表
        #             if live_name.find('淘宝') != -1:
        #                 pass
        #             elif live_name.find('京东') != -1:
        #                 pass
        #             elif live_name.find('抖音') != -1:
        #                 pass
        #             elif live_name.find('快手') != -1:
        #                 pass
        #             elif live_name.find('苏宁') != -1:
        #                 pass
        #         # 判断是不是更新
        #         else:
        #             # 判断当是更新时的图文表
        #             if live_name.find('淘宝') != -1:
        #                 pass
        #                 # qtimage = QitengTaobaoImageTextOffer.query.filter(QitengTaobaoImageTextOffer.id == user_id).first()
        #             elif live_name.find('京东') != -1:
        #                 pass
        #             elif live_name.find('抖音') != -1:
        #                 pass
        #             elif live_name.find('快手') != -1:
        #                 pass
        #             elif live_name.find('苏宁') != -1:
        #                 pass
        #         qtimage.fans_less = int(args.get('fans_less', 0))
        #         qtimage.fans_more = int(args.get('fans_more', 0))
        #         qtimage.image_text_offer = int(args.get('image_text_offer', 0))
        #         qtimage.image_text_cost_price = int(args.get('image_text_cost_price', 0))
        #         qtimage.remarks = args.get('remarks', None)
        #
        #         if status == 'update':
        #             for item in qtimage.image_texts:
        #                 item.image_text_offer = int(args.get('image_text_offer', 0))
        #                 item.image_text_cost_price = int(args.get('image_text_cost_price', 0))
        #                 try:
        #                     item.save(item)
        #                 except Exception as e:
        #                     print('Image_Text save fail', e)
        #                     return e
        #         try:
        #             qtimage.save(qtimage)
        #         except Exception as e:
        #             print('Image_Text_price save fail', e)
        #             return e
        elif live_name=='个性匹配小红书':

            self.parse.add_argument('image_offer', type=int)
            self.parse.add_argument('image_cost_price', type=int)
            self.parse.add_argument('video_offer', type=int)
            self.parse.add_argument('viedo_cost_price', type=int)
            self.parse.add_argument('fans_less', type=float)
            self.parse.add_argument('fans_more', type=float)
            self.parse.add_argument('remarks', type=str)
            self.parse.add_argument('brand_partner', type=str)
            self.parse.add_argument('brand_image_offer', type=int)
            self.parse.add_argument('brand_image_cost_price', type=int)
            self.parse.add_argument('brand_video_offer', type=int)
            self.parse.add_argument('brand_viedo_cost_price', type=int)

            args = self.parse.parse_args()

            if action == 'create':
                qtmatchredbook = QitengRedbookPrice()

            # 判断是不是更新
            else:
                qtmatchredbook = QitengRedbookPrice.query.filter(QitengRedbookPrice.id == user_id).first()
            qtmatchredbook.fans_less = 0 if not args.get('fans_less') else args.get('fans_less')
            qtmatchredbook.fans_more = 0 if not args.get('fans_more') else args.get('fans_more')
            qtmatchredbook.image_offer = 0 if not args.get('image_offer') else args.get('image_offer')
            qtmatchredbook.image_cost_price = 0 if not args.get('image_cost_price') else args.get('image_cost_price')
            qtmatchredbook.video_offer = 0 if not args.get('video_offer') else args.get('video_offer')
            qtmatchredbook.viedo_cost_price = 0 if not args.get('viedo_cost_price') else args.get('viedo_cost_price')
            qtmatchredbook.brand_image_offer = 0 if not args.get('brand_image_offer') else args.get('brand_image_offer')
            qtmatchredbook.brand_image_cost_price = 0 if not args.get('brand_image_cost_price') else args.get('brand_image_cost_price')
            qtmatchredbook.brand_video_offer = 0 if not args.get('brand_video_offer') else args.get('brand_video_offer')
            qtmatchredbook.brand_viedo_cost_price = 0 if not args.get('brand_viedo_cost_price') else args.get('brand_viedo_cost_price')
            qtmatchredbook.remarks ='' if not args.get('remarks') else args.get('remarks')
            qtmatchredbook.brand_partner = True if  args.get('brand_partner')=='true' else False
            if action == 'update':
                for item in qtmatchredbook.redbooks:
                    if item:
                        if item.brand_partner:
                            item.offer_image_text = 0 if not args.get('image_offer') else args.get('image_offer')
                            item.cost_price_image_text = 0 if not args.get('image_cost_price') else args.get('image_cost_price')
                            item.red_book_offer_video = 0 if not args.get('video_offer') else args.get('video_offer')
                            item.red_book_cost_price_video = 0 if not args.get('viedo_cost_price') else args.get('viedo_cost_price')
                        else:
                            item.offer_image_text = 0 if not args.get('brand_image_offer') else args.get('brand_image_offer')
                            item.cost_price_image_text = 0 if not args.get('brand_image_cost_price') else args.get('brand_image_cost_price')
                            item.red_book_offer_video = 0 if not args.get('brand_video_offer') else args.get('brand_video_offer')
                            item.red_book_cost_price_video = 0 if not args.get('brand_viedo_cost_price') else args.get('brand_viedo_cost_price')
                        try:
                            item.save(item)
                        except Exception as e:
                            print('QitengRedbookPrice save fail', e)
                            return e
            try:
                qtmatchredbook.save(qtmatchredbook)
            except Exception as e:
                print('Redbook save fail', e)
                return e

class ShowResource(Resource):

    select_dict = {1: '直播淘宝', 2: '直播抖音', 3: '直播快手', 4: '直播苏宁',
                   5: '短视频淘宝', 6: '短视频抖音', 7: '短视频快手', 8: '短视频苏宁',
                   9: '图文淘宝', 10: '图文抖音', 11: '图文快手', 12: '图文苏宁',
                   13: '个性匹配小红书',14:''}

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('page', type=str)
        self.parse.add_argument('limit', type=str)
        self.parse.add_argument('user_id', type=str)
        self.parse.add_argument('flag', type=str)
        self.parse.add_argument('select_type', type=int)

    def get(self):
        print('resourceshow args get',)
        dic = {}
        args = self.parse.parse_args()
        flag = '直播淘宝' if not args.get('flag') else args.get('flag')
        select_type = 14 if not args.get('select_type') else int(args.get('select_type'))
        page = 1 if not args.get('page') else int(args.get('page'))
        limit =20 if not args.get('limit') else int(args.get('limit'))

        select = self.select_dict.get(select_type, '直播淘宝')
        print('resourcetable flag select_type', flag, select_type)
        print('resourcetable args get', args)
        if select:
            flag =select
        print(flag)
        all_list = []
        totle = 0
        # 直播
        if flag.startswith('直播'):
            print('直播')
            live_query = Live.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:2]),ResourceTable.platform==flag[2:]).offset((page - 1) * limit).limit(limit).all()
            totle = Live.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:2],ResourceTable.platform==flag[2:])).count()
            print('live_query',live_query)
            for item in live_query:
                print('item',item)
                dict = {}
                dict['live'] = Live.queryToDict(item)
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                if flag.find('淘宝') != -1:
                    print('淘宝')
                    livetaobaoprice_query = QitengTaobaoLiveOffer.query.filter(
                        QitengTaobaoLiveOffer.id == item.qiteng_taobao_live_offer_id).first()
                    if livetaobaoprice_query:
                        dysl_dict = QitengTaobaoLiveOffer.queryToDict(livetaobaoprice_query)
                        for k, v in dysl_dict.items():
                            dict['live'][k] = v
                dict['live'].update(dict['rsst'])
                all_list.append(dict['live'])
                # all_list.append(dict)

        # 短视频
        elif flag.startswith('短视频') :
            print('短视频')
            live_query = ShortVideo.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:3],ResourceTable.platform==flag[3:])).offset((page - 1) * limit).limit(limit).all()
            totle = ShortVideo.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:3],ResourceTable.platform==flag[3:])).count()
            for item in live_query:
                dict = {}
                dict['video'] = Live.queryToDict(item)
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                if flag.find('抖音') != -1:
                    videoprice_query = QitengDouyinVideoOffer.query.filter(
                        QitengDouyinVideoOffer.id == item.qiteng_douyin_video_offer_id).first()
                    if videoprice_query:
                        video_dict = QitengDouyinVideoOffer.queryToDict(videoprice_query)
                        for k, v in video_dict.items():
                            dict['video'][k] = v
                dict['video'].update(dict['rsst'])
                all_list.append(dict['video'])

        # 图文
        elif flag.startswith('图文') :
            print('图文')
            image_query = ImageText.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:2],ResourceTable.platform==flag[2:])).offset((page - 1) * limit).limit(limit).all()
            totle = ImageText.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:2],ResourceTable.platform==flag[2:])).count()
            for item in image_query:
                dict = {}
                dict['image'] = ImageText.queryToDict(item)
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                dict['image'].update(dict['rsst'])
                all_list.append(dict['image'])

        # 个性匹配
        elif flag.startswith('个性匹配') :
            print('个性匹配')
            live_query = Redbook.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:4],ResourceTable.platform==flag[4:])).offset((page - 1) * limit).limit(limit).all()
            totle = Redbook.query.join(ResourceTable).filter(and_(ResourceTable.cooperation_type==flag[0:4],ResourceTable.platform==flag[4:])).count()
            for item in live_query:
                dict = {}
                dict['redbook'] = Redbook.queryToDict(item)
                res_query = item.resource_table
                if res_query:
                    res_dict = ResourceTable.queryToDict(res_query)
                    dict['rsst'] = res_dict
                if flag.find('小红书') != -1 :
                    redbook_price_query = QitengRedbookPrice.query.filter(
                        QitengRedbookPrice.id == item.qiteng_redbook_price_id).first()
                    if redbook_price_query:
                        redbook_dict = QitengRedbookPrice.queryToDict(redbook_price_query)
                        for k, v in redbook_dict.items():
                            dict['redbook'][k] = v
                dict['redbook'].update(dict['rsst'])
                all_list.append(dict['redbook'])

        print('all_list', json.dumps({'code': 20000, 'data': {'total': totle, 'items': all_list}}, ensure_ascii=False))
        return jsonify({'code': 20000, 'data': {'total': totle, 'items': all_list}})


ResourceApi.add_resource(TotalResource, '/resourcetable')
ResourceApi.add_resource(PriceResource ,'/resourceprice')
ResourceApi.add_resource(ShowResource, '/resourceshow')
# ResourceApi.add_resource(TaobaoExportLiveOffer, '/taobaoexportliveprice')
# ResourceApi.add_resource(RedbookPrice, '/redbookprice')
# ResourceApi.add_resource(DouyinShoryViewPrice, '/douyinshortviewprice')