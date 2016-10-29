# coding=utf-8
import _env
from solo.web.mongo import Doc
from app.leadhug.controller.model_interface.report_new import ReportInterface
from app.leadhug.controller.tools import DateTime, Tool
import datetime
import time as _time
from datetime import timedelta
from app.leadhug.model.report_day import ReportDay


class ReportHour(Doc, ReportInterface):
    '''
     data display report every hour
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
        hour=str,   # for example: 0, 1, 2, 3, ..., 23
        day=str,    # for example: 2016-03-12
        week=str,   # for example: 2016_10  notice: 10 mean that it's the tenth week of 2016
        month=str,  # for example: 2016-10
        year=str,   # for example: 2016
    )

    @classmethod
    def aggregate(cls, *args, **kwds):
        # result = []
        # for i in cls._collection.aggregate(*args, **kwds):
        #     # i['_id'] = str(i['_id'])
        #     result.append(i)
        # return map(lambda doc: cls(doc, collection=cls._collection), result)
        return cls._collection.aggregate(*args, **kwds)

    @classmethod
    def get_highcharts_data(cls, time, user_id):
        _d = DateTime
        reports = {}
        today = datetime.date.today().strftime('%Y-%m-%d')
        if time == 'today':
            reports = ReportHour.aggregate([
                {'$match': {'affiliate_id': user_id, 'day': today}},
                {'$group': {'_id': '$hour', 'clicks': {'$sum': '$clicks'}, 'conversions': {'$sum': '$conversions'}}},
                {'$sort': {'_id': 1}}
            ]
            )
        if time == '7days':
            reports = ReportDay.aggregate([
                {'$match': {'affiliate_id': user_id, 'day': {'$gte': _d.get_day_date(7).strftime('%Y-%m-%d'), '$lte': today}}},
                {'$group': {'_id': '$day', 'clicks': {'$sum': '$clicks'}, 'conversions': {'$sum': '$conversions'}}},
                {'$sort': {'_id': 1}}
            ]
            )
        if time == '14days':
            reports = ReportDay.aggregate([
                {'$match': {'affiliate_id': user_id, 'day': {'$gte': _d.get_day_date(14).strftime('%Y-%m-%d'), '$lte': today}}},
                {'$group': {'_id': '$day', 'clicks': {'$sum': '$clicks'}, 'conversions': {'$sum': '$conversions'}}},
                {'$sort': {'_id': 1}}
            ]
            )
        if time == '8weeks':
            year = datetime.date.today().strftime('%Y')
            now_week = _time.strftime('%W')
            delay = timedelta(weeks=7)
            past_week = (datetime.datetime.now() - delay).strftime("%W")
            reports = ReportDay.aggregate([
                {'$match': {'affiliate_id': user_id, 'week': {'$gte': year+'_'+past_week, '$lte': year+'_'+now_week}}},
                {'$group': {'_id': '$week', 'clicks': {'$sum': '$clicks'}, 'conversions': {'$sum': '$conversions'}}},
                {'$sort': {'_id': 1}}
            ]
            )
        return reports


if __name__ == '__main__':
    report = ReportHour(
        dict(
            _id=3,
            affiliate_name='test',
            affiliate_id=25,
            affiliate_sub_id_1=1.1,
            affiliate_sub_id_2=1.2,
            affiliate_sub_id_3=1.3,
            affiliate_sub_id_4=1.4,
            affiliate_sub_id_5=1.5,
            offer_name='myoffer',
            offer_id=6,
            advertiser_name='jay',
            advertiser_id=23,
            category_name='app',
            category_id=1,
            country='US',
            impressions=1,
            gross_clicks=2000,
            unique_clicks=200,
            clicks=1000,
            conversions=100,
            cost=88.8,
            revenue=100,
            sales=10,
            profit=44.4,
            hour='12',   # for example: 0, 1, 2, 3, ..., 23
            day='2016-03-28',    # for example: 2016-03-12
            week='2016_10',   # for example: 2016_10  notice: 10 mean that it's the tenth week of 2016
            month='2016_3',  # for example: 2016-10
            year='2016',
        )
    )
    report.save()
