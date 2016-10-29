# coding=utf-8
import sys
import os
path = os.path.join(os.getcwd(), "../../")
sys.path.append(path)
import _env  # noqa
from app.leadhug.model.report_day import ReportDay
from app.leadhug.model.report_hour import ReportHour
from mongokit import Connection, INDEX_DESCENDING, INDEX_ASCENDING
from solo.config import MONGO_CONFIG
from bson.code import Code
from pymongo import Connection as conn


class CreateIndex(object):

    def __init__(self):
        self.db = Connection(MONGO_CONFIG.get('host')).leadhug

    def create(self):
        report_condition_indexs = [
            ('day', INDEX_DESCENDING),
            ('affiliate_id', INDEX_DESCENDING),
            ('offer_id', INDEX_DESCENDING),
            ('advertiser_id', INDEX_DESCENDING),
            ('country', INDEX_DESCENDING),
            ('payout_type', INDEX_DESCENDING),
            ('category_name', INDEX_DESCENDING),
        ]

        report_group_indexs = [
            'affiliate_id',
            'affiliate_name',
            'affiliate_sub_id_1',
            'affiliate_sub_id_2',
            'affiliate_sub_id_3',
            'affiliate_sub_id_4',
            'affiliate_sub_id_5',
            'offer_id',
            'offer_name',
            'advertiser_id',
            'advertiser_name',
            'category_name',
            'country',
            'day',
            'week',
            'month',
            'year'
        ]

        self.db.reportDay.ensure_index(report_condition_indexs)
        for group_index in report_group_indexs:
            self.db.reportDay.ensure_index([(group_index, INDEX_DESCENDING)])

        self.db.reportHour.ensure_index(report_condition_indexs)
        report_group_indexs.insert(-4, 'hour')
        for group_index in report_group_indexs:
            self.db.reportHour.ensure_index([(group_index, INDEX_DESCENDING)])


if __name__ == '__main__':
    # CreateIndex().db.reportDay.drop_indexes()
    obj = CreateIndex().db.reportDay
    for i in range(100000, 1000000):
        obj.insert({
                "_id" : i,
                "advertiser_id" : 821,
                "advertiser_name" : "SOLO",
                "affiliate_id" : 64,
                "affiliate_name" : "Roman Leontev",
                "affiliate_sub_id_1" : 15,
                "affiliate_sub_id_2" : 12,
                "affiliate_sub_id_3" : "",
                "affiliate_sub_id_4" : "",
                "affiliate_sub_id_5" : "",
                "category_name" : "APP Download Android",
                "clicks" : 0,
                "conversions" : 1,
                "cost" : 0.24,
                "country" : "Trinidad And Tobago",
                "day" : "2016-05-17",
                "gross_clicks" : 0,
                "hour" : 23,
                "impressions" : 0,
                "month" : 10,
                "offer_id" : 10156,
                "offer_name" : "Wi-Fi tools-Android-Nonincent-WW except PK and BD",
                "profit" : 0.06,
                "revenue" : 0.3,
                "sales" : 0,
                "unique_clicks" : 0,
                "week" : 201544,
                "year" : 2015
        }
)