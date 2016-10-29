# coding=utf-8
import _env
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey
from app.leadhug.controller.model_interface.report_new import ReportInterface


class ReportDay(Doc, ReportInterface):
    '''
     data display report for every day
    '''
    structure = dict(
        _id=int,
        affiliate_name=str,
        affiliate_id=int,
        affiliate_sub_id_1=str,
        affiliate_sub_id_2=str,
        affiliate_sub_id_3=str,
        affiliate_sub_id_4=str,
        affiliate_sub_id_5=str,
        offer_name=str,
        offer_id=int,
        advertiser_name=str,
        advertiser_id=int,
        category_name=str,
        category_id=int,
        country=str,
        impressions=int,
        gross_clicks=int,
        unique_clicks=int,
        clicks=int,
        conversions=int,
        cost=float,
        revenue=float,
        sales=int,
        profit=float,
        day=str,    # for example: 2016-03-12
        week=str,   # for example: 2016_10  notice: 10 mean that it's the tenth week of 2016
        month=str,  # for example: 2016-10
        year=str,   # for example: 2016
    )

    @classmethod
    def aggregate(cls, *args, **kws):
        return cls._collection.aggregate(*args, **kws)

if __name__ == '__main__':
    pass
