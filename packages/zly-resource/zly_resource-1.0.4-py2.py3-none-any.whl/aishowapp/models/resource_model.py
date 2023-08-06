# # -*- coding: utf-8 -*-
# from sqlalchemy import String, Integer, Column, ForeignKey, BigInteger, Float, Boolean
#
# from aishowapp.ext import db
# from aishowapp.models import BaseDef
# from config import USE
#
#
#
# # 资源总表
# class ResourceTable(db.Model, BaseDef):
#
#     """
#     资源总表
#     """
#
#     __tablename__ = 'resource_table'
#
#     id = db.Column(db.BigInteger, primary_key=True)
#     kol_name = db.Column(db.String(128), nullable=False, unique=True)
#     kol_id = db.Column(db.String(128), nullable=False, unique=True, comment='达人平台ID')
#     str = db.Column(db.String(128), default='男', comment='性别')
#     platform = db.Column(db.String(128), nullable=False, comment='平台')
#     cooperation_type = db.Column(db.String(128), nullable=False, comment='合作模式')
#     fans = db.Column(db.Float, nullable=False, comment='粉丝数/万')
#     total_sell_money = db.Column(db.String(255), comment='与麒腾累计带货合作金额')
#     cooperation_times = db.Column(db.Integer, comment='合作次数')
#     status = db.Column(db.Integer, comment='状态') #0:待审核,1:有效,-1:停用
#     hierarchy = db.Column(db.String(64), comment='层级') #优质、腰部、头部、超头部
#
#     # company = db.Column(db.String(128), comment='所属公司')
#     # contact_name = db.Column(db.String(128), comment='联系人')
#     # contact_phone = db.Column(db.String(128), comment='电话')
#
#     redbook_image_text_links = db.relationship('RedbookImageTextLink', backref='resource_table')
#     douyin_view_exports = db.relationship("DouyinViewExport", backref='resource_table')
#     douyin_special_lives = db.relationship("DouyinSpecialLive", backref='resource_table')
#     douyin_single_chain_lives = db.relationship("DouyinSingleChainLive", backref='resource_table')
#     taobao_lives = db.relationship("TaobaoLive", backref='resource_table')
#     kuai_show_lives = db.relationship("KuaiShouLive", backref='resource_table')
#
#
# #小红书图文链接
# class RedbookImageTextLink(db.Model, BaseDef):
#
#     __tablename__ = 'redbook_image_text_link'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     dianzan = db.Column(db.Integer, default=0, comment='点赞量级/万')
#     redbook_link = db.Column(db.String(255), nullable=False, unique=True, comment='链接')
#     export_city = db.Column(db.String(255), comment='达人所在城市')
#     export_tag = db.Column(db.String(128), default=0, comment='达人标签')
#     brand_partner = db.Column(db.Boolean, default=False, comment='是否品牌合作人')
#     redbook_cost_price = db.Column(db.Integer, default=0, comment='成本价')
#     redbook_offer = db.Column( db.Integer,default=0,comment='小红书报价')
#     qiteng_redbook_price_id =  db.Column( db.BigInteger,  db.ForeignKey('qiteng_redbook_price.id', ondelete='CASCADE',
#                                                                onupdate='CASCADE'))
#
# # 麒腾小红书3月报价
# class QitengRedbookPrice(db.Model,BaseDef):
#
#     """
#     麒腾小红书3月报价表
#     """
#
#     __tablename__ = 'qiteng_redbook_price'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     fans_less = db.Column(db.Integer, default=0, comment='粉丝量级最低/万')
#     fans_more = db.Column(db.Integer, default=0, comment='粉丝量级最高/万')
#     offer_less = db.Column(db.Integer, default=0, comment='报价最低值')
#     offer_more = db.Column(db.Integer, default=0, comment='报价最高值')
#     cost_price = db.Column(db.Integer, default=0, comment='成本价')
#     remarks = db.Column(db.String(255), comment='备注')
#     brand_partner = db.Column(db.Boolean, default=False, comment='是否品牌合作人')
#     brand_partner_offer_less = Column(Integer, default=0,comment='品牌合作人报价区间最低值')
#     brand_partner_offer_more = Column(Integer, default=0,comment='品牌合作人报价区间最高值')
#     brand_partner_cost_price = Column(Integer, default=0,comment='品牌合作人成本价')
#     brand_partner_remarks = Column(String(255),nullable=True,comment='品牌合作人备注')
#     redbook_image_text_links = db.relationship('RedbookImageTextLink', backref='qiteng_redbook_price',)
#
#
# #抖音达人分类
# class DouyinExportClassification(db.Model, BaseDef):
#
#     """
#     抖音达人分类
#     """
#     __tablename__ = 'douyin_export_classification'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     classification_description = db.Column(db.String(64),unique=True,comment='分类描述')
#     # douyin_view_exports = db.relationship('DouyinViewExport', backref='douyin_export_classification', )
#
# #抖音短视频达人表
# class DouyinViewExport(db.Model, BaseDef):
#
#     """
#     抖音短视频达人表
#     """
#
#     __tablename__ = 'douyin_view_export'
#     __bind_key__ = USE
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     # douyin_export_classification = db.Column(db.String(255),  comment='类目属性')
#     export_tag = db.Column(db.String(255),  comment='达人标签')
#     introduction = db.Column(db.String(255), comment='简介')
#     douyin_home_page = db.Column(db.String(255), nullable=False, unique=True, comment='抖音主页url')
#     export_city = db.Column(db.String(255),  comment='达人所在城市')
#     cooperation_case = db.Column(db.String(255),  comment='达人合作过的品牌')
#     better_sell_goods = db.Column(db.String(255),  comment='达人销售过较好的商品')
#     douyin_export_classification = db.Column(db.String(255), comment='抖音达人分类')
#     cooperation_mode = db.Column(db.String(255), nullable=False, comment='合作模式')
#     offer_less = db.Column(db.Integer, default=0, comment='报价区间最低值')
#     offer_more = db.Column(db.Integer, default=0, comment='报价区间最高值')
#     star_offer = db.Column(db.Integer, default=0, comment='星图参考报价最高')
#     douyin_view_cost_price = db.Column(db.Integer, default=0, comment='成本价')
#     qiteng_douyin_view_price_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_douyin_view_price.id', ondelete='CASCADE',
#                                                           onupdate='CASCADE'))
#
# #麒腾抖音短视频3月报价
# class QitengDouyinViewPrice(db.Model, BaseDef):
#
#     """
#     麒腾抖音短视频3月报价
#     """
#     __tablename__ = 'qiteng_douyin_view_price'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     fans_less = db.Column(db.Float, default=0, comment='粉丝量级区间最低')
#     fans_more = db.Column(db.Float, default=0, comment='粉丝量级区间最高')
#     offer_less = db.Column(db.Integer, default=0, comment='报价区间最低值')
#     offer_more = db.Column(db.Integer, default=0, comment='报价区间最高值')
#     star_offer_less = db.Column(db.Integer, default=0, comment='星图参考报价最低')
#     star_offer_more = db.Column(db.Integer, default=0, comment='星图参考报价最低')
#     estimated_exposure = db.Column(db.Float, default=0, comment='预估曝光')
#     remarks = db.Column(db.String(255), nullable=False, comment='备注')
#     cost_price = db.Column(db.Integer, default=0,comment='成本价')
#     douyin_view_exports= db.relationship('DouyinViewExport', backref='qiteng_douyin_view_price')
#
#
#
# #抖音专场直播
# class DouyinSpecialLive(db.Model, BaseDef):
#
#     """
#     抖音专场直播表
#     """
#     __tablename__ = 'douyin_special_live'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     export_tag = db.Column(db.String(128), nullable=False, comment='达人标签')
#     special_offer = db.Column(db.Integer, default=0, comment='专场报价区间最低值')
#     export_city = db.Column(db.String(64), comment='达人所在城市')
#     cooperation_case = db.Column(db.String(255),  comment='达人合作过的品牌')
#     douyin_special_cost_price = db.Column(db.Integer, default=0, comment='成本价')
#
#
# #抖音单链直播
# class DouyinSingleChainLive(db.Model, BaseDef):
#
#     """
#     抖音单链直播表
#     """
#     __tablename__ = 'douyin_single_chain_live'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     douyin_export_classification = db.Column(db.String(255), nullable=False, comment='抖音大类')
#     Single_chain_offer = db.Column(db.Integer, default=0, comment='单链接报价区间')
#     introduction = db.Column(db.String(255), comment='简介')
#     selection_requirements = db.Column(db.String(255), nullable=False, comment='选品要求')
#     live_time = db.Column(db.String(64), comment='直播时间')
#     remarks = db.Column(db.String(255), comment='备注')
#     douyin_single_cost_price = db.Column(db.Integer, default=0, comment='成本价')
#
#
# #淘宝直播
# class TaobaoLive(db.Model, BaseDef):
#
#     """
#      淘宝直播表
#      """
#     __tablename__ = 'taobao_live'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     avg_viewing_num = db.Column(db.Float, default=0, comment='场均观看/小时')
#     main_category = db.Column(db.String(64), nullable=False, comment='主营类目')
#     introduction = db.Column(db.String(255), comment='简介')
#     taobao_offer = db.Column(db.Integer, default=0, comment='淘宝直播报价')
#     taobao_cost_price = db.Column(db.Integer, default=0, comment='淘宝直播成本价')
#     qiteng_taobao_export_live_offer_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_taobao_export_live_offer.id', ondelete='CASCADE',
#                                                    onupdate='CASCADE'))
#
# #麒腾淘宝KOL直播报价
# class QitengTaobaoExportLiveOffer(db.Model, BaseDef):
#
#     """
#     麒腾淘宝KOL直播报价表
#     """
#     __tablename__ = 'qiteng_taobao_export_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     hierarchy = db.Column(db.String(64), nullable=False, comment='层级')
#     avg_viewing_num_less = db.Column(db.Float, default=0, comment='场均观看量级低')
#     avg_viewing_num_more = db.Column(db.Float, default=0, comment='场均观看量级高')
#     offer_less = db.Column(db.Integer, default=0, comment='最低报价')
#     offer_more = db.Column(db.Integer, default=0, comment='最高报价')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#     cost_price = db.Column(db.Integer, default=0, comment='成本价')
#     taobao_lives = db.relationship('TaobaoLive', backref='qiteng_taobao_export_live_offer')
#
#
# # 快手直播
# class KuaiShouLive(db.Model, BaseDef):
#
#     """
#     快手直播
#     """
#
#     __tablename__ = 'kuai_show_live'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     resource_table_id = db.Column(db.BigInteger,
#                                   db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
#     avg_online_num = db.Column(db.Float, default=0, comment='平均在线人数/万')
#     sell_classification = db.Column(db.String(255), nullable=False, comment='可售卖类目')
#     commission_less = db.Column(db.Integer, default=0, comment='佣金最低范围最低')
#     commission_more = db.Column(db.Integer, default=0, comment='佣金最高范围最高')
#     attributes = db.Column(db.String(64), nullable=False, comment='属性')
#     kuaishou_offer = db.Column(db.Integer, default=0, comment='快手报价')
#     kuaishou_cost_price = db.Column(db.Integer, default=0, comment='快手成本价')
#     remarks = db.Column(db.String(255), comment='备注')