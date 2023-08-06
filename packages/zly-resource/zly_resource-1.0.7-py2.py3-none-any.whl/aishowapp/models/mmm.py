# -*- coding: utf-8 -*-
from datetime import datetime as cdatetime
from datetime import date, time
from flask_sqlalchemy import Model
from sqlalchemy import DateTime, Numeric, Time, Date
from aishowapp.ext import db

# class Contract(db.Model):
#     """
#     合同
#     """
#     __tablename__ = 'contract'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     mcn_id = db.Column(db.Integer, db.ForeignKey('mcn.id'))
#     # mcn = relationship("Mcn",back_populates="contract_mcn",  foreign_keys=[mcn_id])
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     # order = relationship("Order", back_populates="contrac_order", foreign_keys=[order_id])
#     type = db.Column(db.String(64))
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
#     amount_received = db.Column(db.Integer,comment='到账金额')
#     risk = db.Column(db.String(64),comment='风险评估')
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
#     sign_stafff = db.Column(db.Integer, db.ForeignKey("users.id"),comment='签约人')
#     contract_number = db.Column(db.String(64),comment='合同编号')
#     sum = db.Column(db.Float,default=0,comment='总成本')
#     start_time = db.Column(db.DateTime,comment='开始执行时间')
#     end_time= db.Column(db.DateTime,comment='到账时间')
#     contract_intro = db.Column(db.String(64),comment='合同回转情况')
#     reason = db.Column(db.String(64),comment='提前执行缘由')
#     other_intro = db.Column(db.String(64),comment='其他情况说明')
#     approval_number = db.Column(db.String(64),comment='审批编号')
#     upload_image_id = db.Column(db.Integer, db.ForeignKey('upload_image.id'),comment='上传合同')
#     project = db.relationship("Project", backref="contract")
#     contract_name = db.Column(db.String(64),comment='合同简称')

class BaseDef(object):

    @classmethod
    def queryToDict(cls, models):
        if (isinstance(models, list)):
            if (isinstance(models[0], Model)):
                lst = []
                for model in models:
                    gen = cls.model_to_dict(model)
                    # print('gen',gen)
                    dit = dict((g[0], g[1]) for g in gen)
                    lst.append(dit)
                return lst
            else:
                res = cls.result_to_dict(models)
                return res
        else:
            if (isinstance(models, Model)):
                gen = cls.model_to_dict(models)
                dit = dict((g[0], g[1]) for g in gen)
                return dit
            else:
                res = dict(zip(models.keys(), models))
                cls.find_datetime(res)
                return res

    # 当结果为result对象列表时，result有key()方法
    @classmethod
    def result_to_dict(cls, results):
        res = [dict(zip(r.keys(), r)) for r in results]
        # 这里r为一个字典，对象传递直接改变字典属性
        for r in res:
            cls.find_datetime(r)
        return res

    @classmethod
    def model_to_dict(cls, model):  # 这段来自于参考资源
        for col in model.__table__.columns:
            # print('model_to_dict',)
            # print(col)
            if isinstance(col.type, DateTime):
                value = cls.convert_datetime(getattr(model, col.name))
            elif isinstance(col.type, Numeric):
                if getattr(model, col.name):
                    # print(getattr(model, col.name))
                    # print(type(getattr(model, col.name)))
                    value = float(getattr(model, col.name))
            else:
                value = getattr(model, col.name)
            yield (col.name, value)

    @classmethod
    def find_datetime(cls, value):
        for v in value:
            if (isinstance(value[v], cdatetime)):
                value[v] = cls.convert_datetime(value[v])

    @classmethod
    def convert_datetime(cls, value):
        if value:
            if (isinstance(value, (cdatetime, DateTime))):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif (isinstance(value, (date, Date))):
                return value.strftime("%Y-%m-%d")
            elif (isinstance(value, (Time, time))):
                return value.strftime("%H:%M:%S")
        else:
            return ""

    def save(self,obj):
        try:
            db.session.add(obj)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            print('save fail',e)


class ResourceTable(db.Model,BaseDef):

        """
        资源总表
        """

        __tablename__ = 'resource_table'

        id = db.Column(db.BigInteger, primary_key=True)
        kol_name = db.Column(db.String(128),nullable=False,unique=True)
        kol_id = db.Column(db.String(128),nullable=False,unique=True,comment='达人平台ID')
        platform = db.Column(db.String(128),nullable=False,comment='平台')
        avatar = db.Column(db.String(128),nullable=True,comment='头像')
        type_datil = db.Column(db.String(128),nullable=False,comment='合作模式')
        company = db.Column(db.String(128),nullable=True,comment='所属公司')
        contact_name = db.Column(db.String(128),nullable=True,comment='联系人')
        contact_phone = db.Column(db.String(128),nullable=True,comment='电话')
        fans = db.Column(db.Float,nullable=False,comment='粉丝数/万')
        total_sell_money = db.Column(db.String(255),nullable=True,comment='与麒腾累计带货合作金额')
        cooperation_times = db.Column(db.Integer,nullable=True,comment='合作次数')

        redbook_image_text_links = db.relationship('RedbookImageTextLink', backref='resource_table')
        douyin_view_exports = db.relationship("DouyinViewExport", backref='resource_table')
        douyin_special_lives = db.relationship("DouyinSpecialLive", backref='resource_table')
        douyin_single_chain_lives = db.relationship("DouyinSingleChainLive", backref='resource_table')
        taobao_lives = db.relationship("TaobaoLive", backref='resource_table')
        kuai_show_lives = db.relationship("KuaiShouLive", backref='resource_table')


class DouyinExportClassification(db.Model, BaseDef):

    """
    抖音达人分类
    """
    __tablename__ = 'douyin_export_classification'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    classification_description = db.Column(db.String(64),unique=True,comment='分类描述')


class RedbookImageTextLink(db.Model, BaseDef):

    """
    小红书图文链接
    """

    __tablename__ = 'redbook_image_text_link'

    id = db.Column(db.BigInteger, primary_key=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))
    dianzan = db.Column(db.Integer, default=0,comment='点赞量级/万')
    redbook_link = db.Column(db.String(255), nullable=False, unique=True,comment='链接')
    export_city = db.Column(db.String(255), nullable=True,comment='达人所在城市')
    export_tag = db.Column(db.String(128), default=0,comment='达人标签')
    brand_partner = db.Column(db.Boolean, default=False,comment='是否品牌合作人')
    redbook_cost_price = db.Column(db.Integer, default=0,comment='成本价')


class QitengRedbookPrice(db.Model,BaseDef):

    """
     麒腾小红书3月报价表
    """

    __tablename__ = 'qiteng_redbook_price'

    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True,comment='达人平台ID')
    fans_less = db.Column(db.Integer, default=0,comment='粉丝量级最低/万')
    fans_more = db.Column(db.Integer, default=0,comment='粉丝量级最高/万')
    offer_less = db.Column(db.Integer, default=0,comment='报价最低值')
    offer_more = db.Column(db.Integer, default=0,comment='报价最高值')
    cost_price = db.Column(db.Integer, default=0,comment='成本价')
    remarks = db.Column(db.String(255),nullable=True,comment='备注')
    brand_partner= db.Column(db.Boolean, default=False,comment='是否品牌合作人')
    redbook_image_text_link_id = db.Column(db.BigInteger, db.ForeignKey('redbook_image_text_link.id', ondelete='CASCADE',onupdate='CASCADE'))  # 资源表ID
    redbook_image_text_linkid = db.relationship('RedbookImageTextLink', backref='redbook_image_text_links',uselist=False)


class DouyinViewExport(db.Model, BaseDef):

    """
    抖音短视频达人表
    """

    __tablename__ = 'douyin_view_export'

    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))
    douyin_export_classification_id = db.Column(db.BigInteger,db.ForeignKey('douyin_export_classification.id',ondelete='CASCADE', onupdate='CASCADE'))
    export_tag = db.Column(db.String(255),nullable=True,comment='达人标签')
    introduction = db.Column(db.String(255),nullable=True,comment='简介')
    douyin_home_page = db.Column(db.String(255),nullable=False,unique=True,comment='抖音主页url')
    export_city = db.Column(db.String(255),nullable=True,comment='达人所在城市')
    cooperation_case = db.Column(db.String(255),nullable=True,comment='达人合作过的品牌')
    better_sell_goods = db.Column(db.String(255),nullable=True,comment='达人销售过较好的商品')
    douyin_export_classification = db.Column(db.String(255),comment='抖音达人分类')
    cooperation_mode = db.Column(db.String(255),nullable=False,comment='合作模式')
    offer_less = db.Column(db.Integer, default=0,comment='报价区间最低值')
    offer_more = db.Column(db.Integer, default=0,comment='报价区间最高值')
    star_offer = db.Column(db.Integer, default=0,comment='星图参考报价最高')
    douyin_view_cost_price = db.Column(db.Integer, default=0,comment='成本价')



class QitengDouyinViewPrice(db.Model, BaseDef):

    """
    麒腾抖音短视频3月报价
    """

    __tablename__ = 'qiteng_douyin_view_price'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fans_less = db.Column(db.Float, default=0,comment='粉丝量级区间最低')
    fans_more = db.Column(db.Float, default=0,comment='粉丝量级区间最高')
    offer_less = db.Column(db.Integer, default=0,comment='报价区间最低值')
    offer_more = db.Column(db.Integer, default=0,comment='报价区间最高值')
    star_offer_less = db.Column(db.Integer, default=0,comment='星图参考报价最低')
    star_offer_more = db.Column(db.Integer, default=0,comment='星图参考报价最低')
    estimated_exposure = db.Column(db.Float, default=0,comment='预估曝光')
    remarks = db.Column(db.String(255),nullable=False,comment='备注')
    douyin_view_export_id = db.Column(db.BigInteger, db.ForeignKey('douyin_view_export.id', ondelete='CASCADE',
                                                               onupdate='CASCADE'))
    douyin_view_exportid = db.relationship('DouyinViewExport', backref='douyin_view_exports',uselist=False)


class DouyinSpecialLive(db.Model, BaseDef):

    """
    抖音专场直播表
    """
    __tablename__ = 'douyin_special_live'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))
    export_tag = db.Column(db.String(128),nullable=False,comment='达人标签')
    special_offer = db.Column(db.Integer, default=0,comment='专场报价区间最低值')
    export_city = db.Column(db.String(64),nullable=True,comment='达人所在城市')
    cooperation_case = db.Column(db.String(255),nullable=True,comment='达人合作过的品牌')
    douyin_special_cost_price = db.Column(db.Integer, default=0,comment='成本价')


class DouyinSingleChainLive(db.Model, BaseDef):

    """
    抖音单链直播表
    """

    __tablename__ = 'douyin_single_chain_live'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))
    douyin_export_classification = db.Column(db.String(255),nullable=False,comment='抖音大类')
    Single_chain_offer = db.Column(db.Integer, default=0,comment='单链接报价区间')
    introduction = db.Column(db.String(255),nullable=True,comment='简介')
    selection_requirements = db.Column(db.String(255),nullable=False,comment='选品要求')
    live_time = db.Column(db.String(64),comment='直播时间')
    remarks = db.Column(db.String(255), nullable=True,comment='备注')
    douyin_single_cost_price = db.Column(db.Integer, default=0,comment='成本价')



class TaobaoLive(db.Model, BaseDef):

    """
    淘宝直播表
    """

    __tablename__ = 'taobao_live'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))  # 资源表ID
    avg_viewing_num = db.Column(db.Float,default=0,comment='场均观看/小时')
    main_category = db.Column(db.String(64,comment='主营类目'),nullable=False)
    introduction = db.Column(db.String(255), nullable=True,comment='简介')
    taobao_offer = db.Column(db.Integer,default=0,comment='最高')
    taobao_cost_price = db.Column(db.Integer, default=0,comment='成本价')



class QitengTaobaoExportLiveOffer(db.Model, BaseDef):

    """
    麒腾淘宝KOL直播报价表
    """
    __tablename__ = 'qiteng_taobao_export_live_offer'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    hierarchy = db.Column(db.String(64),nullable=False,comment='层级')
    avg_viewing_num_less = db.Column(db.Float,default=0,comment='场均观看量级低')
    avg_viewing_num_more = db.Column(db.Float,default=0,comment='场均观看量级高')
    offer_less = db.Column(db.Integer,default=0,comment='最低报价')
    offer_more = db.Column(db.Integer,default=0,comment='最高报价')
    remarks = db.Column(db.String(255), nullable=True,comment='备注')
    cost_price = db.Column(db.Integer,default=0,comment='成本价')
    taobao_live_id = db.Column(db.BigInteger, db.ForeignKey('taobao_live.id', ondelete='CASCADE',
                                                          onupdate='CASCADE'))
    taobao_liveid = db.relationship('TaobaoLive', backref='taobao_lives',uselist=False)



class KuaiShouLive(db.Model, BaseDef):

    """
    快手直播
    """

    __tablename__ = 'kuai_show_live'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    resource_table_id = db.Column(db.BigInteger, db.ForeignKey('resource_table.id',ondelete='CASCADE', onupdate='CASCADE'))
    avg_online_num = db.Column(db.Float, default=0,comment='平均在线人数/万')
    sell_classification = db.Column(db.String(255),nullable=False,comment='可售卖类目')
    commission_less = db.Column(db.Integer, default=0,comment='佣金最低范围最低')
    commission_more = db.Column(db.Integer, default=0,comment='佣金最高范围最高')
    attributes = db.Column(db.String(64),nullable=False,comment='属性')
    kuaishou_offer = db.Column(db.Integer, default=0,comment='快手报价')
    kuaishou_cost_price = db.Column(db.Integer, default=0,comment='快手成本价')
    remarks = db.Column(db.String(255),nullable=True,comment='备注')