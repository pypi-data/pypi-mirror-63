# -*- coding: utf-8 -*-
from sqlalchemy import String, Integer, Column, ForeignKey, BigInteger, Float, Boolean

from aishowapp.ext import db
from aishowapp.models import BaseDef

USE = 'zly'
#USE = 'wr'


# 资源总表
class ResourceTable(db.Model, BaseDef):

    """
    资源总表
    """
    __tablename__ = 'resource_table'
    __table_args__ = {'extend_existing': True}
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True)
    kol_name = db.Column(db.String(128), nullable=False, unique=True)
    kol_id = db.Column(db.String(128), nullable=False, unique=True, comment='达人平台ID')
    sex = db.Column(db.String(32), default='男', comment='性别')
    platform = db.Column(db.String(128), nullable=False, comment='平台')
    cooperation_type = db.Column(db.String(128), nullable=False, comment='合作模式')
    fans = db.Column(db.Float,default=0, nullable=False, comment='粉丝数/万')
    total_sell_money = db.Column(db.Float,default=0, comment='与麒腾累计带货合作金额')
    cooperation_times = db.Column(db.Integer,default=0, comment='合作次数')
    status = db.Column(db.Integer,default=0, comment='状态') #0:待审核,1:有效,-1:停用
    hierarchy = db.Column(db.String(32), comment='层级') #优质、腰部、头部、超头部

    lives = db.relationship('Live', backref='resource_table')
    short_videos = db.relationship("ShortVideo", backref='resource_table')
    red_books = db.relationship("Redbook", backref='resource_table')
    image_texts = db.relationship("ImageText", backref='resource_table')

#直播
class Live(db.Model, BaseDef):

    """
    直播：淘宝直播，抖音直播，快手直播、苏宁
    """

    __tablename__ = 'live'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True)
    resource_table_id = db.Column(db.BigInteger,
                                  db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
    mechanism = db.Column(db.String(64), nullable=False,comment='机构')
    online_number = db.Column(db.Integer, default=0, comment='在线人数')
    export_city = db.Column(db.String(64), comment='达人所在城市')
    commission = db.Column(db.String(128), default=0, comment='佣金范围')
    selection_classification = db.Column(db.String(255), comment='选品类目')
    avg_viewing_num = db.Column(db.Float, default=0, comment='场均观看/小时')
    single_chain_offer = db.Column(db.Integer, default=0, comment='单链接报价/元')
    single_chain_cost_price = db.Column(db.Integer, default=0, comment='单链接成本价/元')
    special_offer = db.Column(db.Integer, default=0, comment='专场报价/元')
    special_cost_price = db.Column(db.Integer, default=0, comment='专场成本价/元')
    live_time =  db.Column(db.Float, default=0, comment='专场直播时长/小时')
    introduction = db.Column(db.String(255), comment='简介')
    cooperation_case = db.Column(db.String(255), comment='合作案例')
    remarks = db.Column(db.String(255), comment='备注')

    qiteng_taobao_live_offer_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_taobao_live_offer.id',
                                                                         ondelete='CASCADE',onupdate='CASCADE'))
    # qiteng_douyin_live_offer_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_douyin_live_offer.id',
    #                                                                      ondelete='CASCADE', onupdate='CASCADE'))
    # qiteng_kuaishou_live_offer_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_kuaishou_live_offer.id',
    #                                                                      ondelete='CASCADE', onupdate='CASCADE'))
    # qiteng_suning_live_offer_id = db.Column(db.BigInteger, db.ForeignKey('qiteng_suning_live_offer.id',
    #                                                                      ondelete='CASCADE', onupdate='CASCADE'))

#麒腾淘宝KOL直播报价
class QitengTaobaoLiveOffer(db.Model, BaseDef):

    """
    麒腾淘宝KOL直播报价表
    """
    __tablename__ = 'qiteng_taobao_live_offer'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # live_name = db.Column(db.String(64), nullable=False, comment='直播平台名')
    hierarchy = db.Column(db.String(64), nullable=False, comment='层级')
    avg_viewing_num_less = db.Column(db.Float, default=0, comment='场均观看量级低')
    avg_viewing_num_more = db.Column(db.Float, default=0, comment='场均观看量级高')
    single_chain_offer = db.Column(db.Integer, default=0, comment='直播单链接报价/元')
    single_chain_cost_price = db.Column(db.Integer, default=0, comment='直播单链接成本价/元')
    special_offer = db.Column(db.Integer, default=0, comment='直播专场报价/元')
    special_cost_price = db.Column(db.Integer, default=0, comment='直播专场成本价/元')
    remarks = db.Column(db.String(255), nullable=True, comment='备注')

    lives = db.relationship('Live', backref='qiteng_taobao_live_offer')


# #麒腾抖音KOL直播报价
# class QitengDouyinLiveOffer(db.Model, BaseDef):
#
#     """
#     麒腾抖音直播报价表
#     """
#     __tablename__ = 'qiteng_douyin_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     hierarchy = db.Column(db.String(64), nullable=False, comment='层级')
#     avg_viewing_num_less = db.Column(db.Float, default=0, comment='场均观看量级低')
#     avg_viewing_num_more = db.Column(db.Float, default=0, comment='场均观看量级高')
#     single_chain_offer = db.Column(db.Integer, default=0, comment='直播单链接报价/元')
#     single_cost_price = db.Column(db.Integer, default=0, comment='直播单链接成本价/元')
#     special_offer = db.Column(db.Integer, default=0, comment='直播专场报价/元')
#     special_cost_price = db.Column(db.Integer, default=0, comment='直播专场成本价/元')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#
#     lives = db.relationship('Live', backref='qiteng_douyin_live_offer')


# #麒腾快手直播报价
# class QitengKuaishouLiveOffer(db.Model, BaseDef):
#
#     """
#     麒腾快手直播报价
#     """
#     __tablename__ = 'qiteng_kuaishou_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     hierarchy = db.Column(db.String(64), nullable=False, comment='层级')
#     avg_viewing_num_less = db.Column(db.Float, default=0, comment='场均观看量级低')
#     avg_viewing_num_more = db.Column(db.Float, default=0, comment='场均观看量级高')
#     Single_chain_offer = db.Column(db.Integer, default=0, comment='直播单链接报价/元')
#     single_cost_price = db.Column(db.Integer, default=0, comment='直播单链接成本价/元')
#     special_offer = db.Column(db.Integer, default=0, comment='直播专场报价/元')
#     special_cost_price = db.Column(db.Integer, default=0, comment='直播专场成本价/元')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#
#     lives = db.relationship('Live', backref='qiteng_kuaishou_live_offer')


# #麒腾苏宁直播报价
# class QitengSuningLiveOffer(db.Model, BaseDef):
#
#     """
#     麒腾苏宁直播报价
#     """
#     __tablename__ = 'qiteng_suning_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     hierarchy = db.Column(db.String(64), nullable=False, comment='层级')
#     avg_viewing_num_less = db.Column(db.Float, default=0, comment='场均观看量级低')
#     avg_viewing_num_more = db.Column(db.Float, default=0, comment='场均观看量级高')
#     Single_chain_offer = db.Column(db.Integer, default=0, comment='直播单链接报价/元')
#     single_cost_price = db.Column(db.Integer, default=0, comment='直播单链接成本价/元')
#     special_offer = db.Column(db.Integer, default=0, comment='直播专场报价/元')
#     special_cost_price = db.Column(db.Integer, default=0, comment='直播专场成本价/元')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#
#     lives = db.relationship('Live', backref='qiteng_suning_live_offer')


#短视频
class ShortVideo(db.Model, BaseDef):

    """
   短视频：抖音，快手
    """
    __tablename__ = 'short_video'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    resource_table_id = db.Column(db.BigInteger,
                                  db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
    dianzan = db.Column(db.Float, default=0, comment='点赞量/万')
    export_home_page = db.Column(db.String(255), nullable=False, unique=True, comment='达人主页')
    export_tag = db.Column(db.String(255), comment='类型/达人标签')
    export_city = db.Column(db.String(255), comment='达人所在城市')
    cost_0_20s = db.Column(db.Integer, default=0, comment='0-20s成本')
    offer_0_20s = db.Column(db.Integer, default=0, comment='0-20s报价')
    cost_21_60s = db.Column(db.Integer, default=0, comment='21-60s成本')
    offer_21_60s = db.Column(db.Integer, default=0, comment='21-60s报价')
    introduction = db.Column(db.String(255), comment='简介')
    cooperation_case = db.Column(db.String(255), comment='合作案例')
    remarks = db.Column(db.String(255), comment='备注')

    qiteng_douyin_video_offer_id = db.Column(db.BigInteger,
                                  db.ForeignKey('qiteng_douyin_video_offer.id', ondelete='CASCADE', onupdate='CASCADE'))
    # qiteng_kauishou_video_offer_id = db.Column(db.BigInteger,
    #                               db.ForeignKey('qiteng_kauishou_video_offer.id', ondelete='CASCADE', onupdate='CASCADE'))


#麒腾抖音短视频3月报价
class QitengDouyinVideoOffer(db.Model, BaseDef):

    """
    麒腾抖音短视频3月报价
    """

    __tablename__ = 'qiteng_douyin_video_offer'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fans_less = db.Column(db.Float, default=0, comment='粉丝量级区间最低')
    fans_more = db.Column(db.Float, default=0, comment='粉丝量级区间最高')
    cost_0_20s = db.Column(db.Integer, default=0, comment='抖音短视频0-20s成本')
    offer_0_20s = db.Column(db.Integer, default=0, comment='抖音短视频0-20s报价')
    cost_21_60s = db.Column(db.Integer, default=0, comment='抖音短视频21-60s成本')
    offer_21_60s = db.Column(db.Integer, default=0, comment='抖音短视频21-60s报价')
    star_offer_0_20s = db.Column(db.Integer, default=0, comment='星图0_20s参考报价')
    star_offer_21_60s = db.Column(db.Integer, default=0, comment='星图21_60s参考报价')
    estimated_0_20s = db.Column(db.Float, default=0, comment='0_20s预估曝光')
    estimated_21_60s = db.Column(db.Float, default=0, comment='21_60s预估曝光')
    remarks = db.Column(db.String(255), nullable=False, comment='备注')

    short_videos= db.relationship('ShortVideo', backref='qiteng_douyin_video_offer')

# #麒腾快手短视频3月报价
# class QitengKuaishouVideoOffer(db.Model, BaseDef):
#
#     """
#     麒腾快手短视频3月报价
#     """
#
#     __tablename__ = 'qiteng_kauishou_video_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     fans_less = db.Column(db.Float, default=0, comment='粉丝量级区间最低')
#     fans_more = db.Column(db.Float, default=0, comment='粉丝量级区间最高')
#     short_video_offer_less = db.Column(db.Integer, default=0, comment='报价区间最低值')
#     short_video_offer_more = db.Column(db.Integer, default=0, comment='报价区间最高值')
#     cost_0_20s = db.Column(db.Integer, default=0, comment='快手短视频0-20s成本')
#     offer_0_20s = db.Column(db.Integer, default=0, comment='快手短视频0-20s报价')
#     cost_21_60s = db.Column(db.Integer, default=0, comment='快手短视频21-60s成本')
#     offer_21_60s = db.Column(db.Integer, default=0, comment='快手短视频21-60s包价')
#     star_offer_0_20s = db.Column(db.Integer, default=0, comment='快手短视频0_20s星图参考报价')
#     star_offer_21_60s = db.Column(db.Integer, default=0, comment='快手短视频21-60s星图参考报价')
#     estimated_0_20s = db.Column(db.Float, default=0, comment='0_20s预估曝光')
#     estimated_21_60s = db.Column(db.Float, default=0, comment='21_60s预估曝光')
#     remarks = db.Column(db.String(255), nullable=False, comment='备注')
#
#     short_videos = db.relationship('ShortVideo', backref='qiteng_kauishou_video_offer')


#小红书
class Redbook(db.Model, BaseDef):
    """
   小红书
    """
    __tablename__ = 'redbook'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True)
    resource_table_id = db.Column(db.BigInteger,
                                  db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
    export_home_page = db.Column(db.String(255), nullable=False, unique=True, comment='达人主页')
    dianzan = db.Column(db.Integer, default=0, comment='点赞量级/万')
    export_city = db.Column(db.String(255), comment='达人所在城市')
    export_tag = db.Column(db.String(128), default=0, comment='账号类型/达人标签')
    cost_price_image_text = db.Column(db.Integer, default=0, comment='小红书成本价/图文')
    offer_image_text = db.Column(db.Integer, default=0, comment='小红书报价/图文')
    red_book_cost_price_video = db.Column(db.Integer, default=0, comment='小红书成本价/视频')
    red_book_offer_video = db.Column(db.Integer, default=0, comment='小红书报价/视频')
    brand_partner = db.Column(db.Boolean, default=False, comment='是否品牌合作人')
    cooperation_case = db.Column(db.String(255), comment='合作案例')
    remarks = db.Column(db.String(255), comment='备注')

    qiteng_redbook_price_id = db.Column( db.BigInteger,  db.ForeignKey('qiteng_redbook_price.id', ondelete='CASCADE',
                                                               onupdate='CASCADE'))


# 麒腾小红书3月报价
class QitengRedbookPrice(db.Model,BaseDef):

    """
    麒腾小红书3月报价表
    """
    __tablename__ = 'qiteng_redbook_price'
    __bind_key__ = USE
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fans_less = db.Column(db.Float, default=0, comment='粉丝量级最低/万')
    fans_more = db.Column(db.Float, default=0, comment='粉丝量级最高/万')
    image_offer= db.Column(db.Integer, default=0, comment='图文报价')
    image_cost_price = db.Column(db.Integer, default=0, comment='图文成本')
    video_offer= db.Column(db.Integer, default=0, comment='视频报价')
    viedo_cost_price = db.Column(db.Integer, default=0, comment='视频成本价格')
    brand_image_offer = db.Column(db.Integer, default=0, comment='品牌合作人图文报价')
    brand_image_cost_price = db.Column(db.Integer, default=0, comment='品牌合作人图文成本价格')
    brand_video_offer = db.Column(db.Integer, default=0, comment='品牌合作人视频报价')
    brand_viedo_cost_price = db.Column(db.Integer, default=0, comment='品牌合作人视频成本价格')
    remarks = db.Column(db.String(255), comment='备注')
    brand_partner = db.Column(db.Boolean, default=False, comment='是否品牌合作人')

    redbooks = db.relationship('Redbook', backref='qiteng_redbook_price',)


#图文：淘宝图文，京东图文
class ImageText(db.Model, BaseDef):

    """
    图文：淘宝图文，京东图文
    """
    __tablename__ = 'image_text'
    __bind_key__ = USE

    id = db.Column(db.BigInteger, primary_key=True)
    resource_table_id = db.Column(db.BigInteger,
                                  db.ForeignKey('resource_table.id', ondelete='CASCADE', onupdate='CASCADE'))
    mechanism = db.Column(db.String(128), nullable=False, unique=True, comment='机构')
    export_tag = db.Column(db.String(255), comment='频道类型/达人标签')
    export_classification = db.Column(db.String(255), comment='类目/达人分类')
    image_cost_price = db.Column(db.Integer, default=0, comment='图文成本价')
    image_offer = db.Column(db.Integer, default=0, comment='图文报价')
    channel_interpretation = db.Column(db.String(255), comment='渠道解读')
    remarks = db.Column(db.String(255), comment='备注')

    # qiteng_taobao_image_text_offer_id = db.Column(db.BigInteger,
    #                               db.ForeignKey('qiteng_taobao_image_text_live_offer.id', ondelete='CASCADE', onupdate='CASCADE'))
    # qiteng_jd_image_text_offer_id = db.Column(db.BigInteger,
    #                               db.ForeignKey('qiteng_jd_image_text_live_offer.id', ondelete='CASCADE', onupdate='CASCADE'))


# #麒腾淘宝图文直播报价
# class QitengTaobaoImageTextOffer(db.Model, BaseDef):
#
#     """
#     麒腾淘宝图文报价
#     """
#     __tablename__ = 'qiteng_taobao_image_text_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     fans_less = db.Column(db.Integer, default=0, comment='粉丝量级最低/万')
#     fans_more = db.Column(db.Integer, default=0, comment='粉丝量级最高/万')
#     image_text_offer = db.Column(db.Integer, default=0, comment='麒腾淘宝图文报价')
#     image_text_cost_price = db.Column(db.Integer, default=0, comment='麒腾淘宝图文成本价')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#
#     image_texts = db.relationship('ImageText', backref='qiteng_taobao_image_text_live_offer')

#
# #麒腾京东图文报价
# class QitengJdImageTextOffer(db.Model, BaseDef):
#
#     """
#     麒腾京东图文报价
#     """
#     __tablename__ = 'qiteng_jd_image_text_live_offer'
#     __bind_key__ = USE
#
#     id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#     fans_less = db.Column(db.Integer, default=0, comment='粉丝量级最低/万')
#     fans_more = db.Column(db.Integer, default=0, comment='粉丝量级最高/万')
#     image_text_offer = db.Column(db.Integer, default=0, comment='麒腾京东图文报价')
#     image_text_cost_price = db.Column(db.Integer, default=0, comment='麒腾京东图文成本价')
#     remarks = db.Column(db.String(255), nullable=True, comment='备注')
#
#     image_texts = db.relationship('ImageText', backref='qiteng_jd_image_text_live_offer')