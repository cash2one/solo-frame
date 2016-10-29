# coding=utf-8
from collections import OrderedDict, defaultdict
from bson import SON
from bson.code import Code
from solo.config import MONGO_CONFIG
from mongokit import Connection, INDEX_DESCENDING


class ReportInterface(object):

    db = Connection(MONGO_CONFIG.get('host')).leadhug

    @classmethod
    def get_range_data(cls, start, end, fields=None, limit=30, skip=0, **kw):
        '''
            args: fields-->[]
                  start--->'2016-03-12'
                  end--->'2016-03-15'
                  kw---> {...}
        '''
        if fields:
            fields_dict = {}
            [fields_dict.update({field: 1}) for field, value in fields.items() if value]

        condition = cls.create_condition(**kw)
        condition.update({
            'day': {
                '$gte': start.strip(),
                '$lte': end.strip()
            }
        })

        collection = cls.db.reportHour if cls.__name__ == 'ReportHour' else cls.db.reportDay

        total_count, results = cls.get_result(collection, fields_dict, condition)
        # total_count, results = cls.get_result2(collection, fields_dict, condition, limit, skip)

        calculate_result = cls.create_calculate_result(fields_dict, results)
        return calculate_result, total_count

    @classmethod
    def get_result2(cls, collection, fields_dict, match, limit, skip):
        sum_field = cls.create_sum_field(fields_dict)
        groups2 = cls.create_groups2(fields_dict, sum_field)
        total_count = collection.aggregate([
            {"$match": match},
            {"$group": groups2},
            {"$sort": SON([("_id", 1)])},
        ]).get('result').__len__() if not skip else 0
        res = collection.aggregate([
            {"$match": match},
            {"$group": groups2},
            {"$sort": {'day': 1}},
            {"$skip": skip},
            {"$limit": limit}
        ])
        result = res.get('result')
        for r in result:
            fields = r.get('_id')
            r.pop('_id')
            r.update(fields)
        return total_count, result

    @classmethod
    def create_sum_field(cls, field_dict):
        fields = [
            'impressions',
            'clicks',
            'gross_clicks',
            'unique_clicks',
            'conversions',
            'cost',
            'revenue',
            'profit',
            'sales'
        ]

        sum_field = {}
        [sum_field.update({fd: {"$sum": "${}".format(fd)}}) for fd in fields if fd in field_dict]
        return sum_field

    @classmethod
    def create_groups2(cls, fields_dict, sum_field):
        group_fields = [
            'hour',
            'day',
            'week',
            'month',
            'year'
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
            'category_status',
        ]
        groups = {'_id': {}}
        [groups['_id'].update({fd: "${}".format(fd)}) for fd in group_fields if fd in fields_dict]
        groups.update(sum_field)
        return groups

    @classmethod
    def get_result(cls, collection, fields_dict, condition):
        initial = cls.create_initial(fields_dict)
        groups = cls.create_group(fields_dict)
        reducer = cls.create_reducer(initial)
        results = collection.group(key=groups, condition=condition, initial=initial, reduce=reducer, finalize=None)
        return len(results), results

    @classmethod
    def create_reducer(cls, initial):
        prev_str = ''
        for k, v in initial.items():
            prev_str += 'prev.{k} += obj.{k};'.format(k=k)

        reduce_code = 'function(obj, prev){%s}' % prev_str
        return Code(reduce_code)

    @classmethod
    def create_initial(cls, field_dict):
        fields = [
            'gross_clicks',
            'unique_clicks',
            'profit',
            'sales',
            'revenue'
        ]

        initial = dict(
            impressions=0,
            clicks=0,
            cost=0,
            conversions=0
        )
        [initial.update({fd: 0}) for fd in fields if fd in field_dict]
        return initial

    @classmethod
    def create_condition(cls, **kw):
        spec = OrderedDict()
        affiliates = kw.get('affiliates_name')
        if affiliates:
            spec.update(dict(affiliate_id={"$in": [int(aff) for aff in affiliates]}))

        advertisers = kw.get('advertisers_name')
        if advertisers:
            spec.update(dict(advertiser_id={"$in": [int(a) for a in advertisers]}))

        offers = kw.get('offers')
        if offers:
            spec.update(dict(offer_id={"$in": [int(i) for i in offers]}))

        countries = kw.get('countries')
        if countries:
            spec.update(dict(country={"$in": countries}))

        payout_types = kw.get('payout_types')
        if payout_types:
            spec.update(dict(payout_type={"$in": payout_types}))

        # payout_range = kw.get('payout_range')
        # if payout_range:
        #     spec.update(dict(cost={
        #         "$gte": float(payout_range.get('min', 0)),
        #         "$lte": float(payout_range.get('mix', 10000))
        #     }))

        categories = kw.get('categories_name')
        if categories:
            spec.update(dict(category_name={"$in": categories}))

        return spec

    @classmethod
    def create_group(cls, fields_dict):
        group_fields = [
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
            'hour',
            'day',
            'week',
            'month',
            'year'
        ]
        groups = {}
        [groups.update({fd: 1}) for fd in group_fields if fd in fields_dict]
        return groups

    @classmethod
    def create_calculate_result(cls, fields_dict, results):
        calculate_fields = [
            'CPC',
            'CPM',
            'CTR',
            'CR',
            'CPA',
            'RPM',
            'RPC',
            'RPA',
            'EPC'
        ]
        calculate = [fd for fd in calculate_fields if fd in fields_dict]

        def result_upate(r):
            for fd in calculate:
                res = getattr(cls, fd)(r)
                r.update({fd: res})
            return r

        results = map(result_upate, results)

        return results

    @classmethod
    def total(cls, datas, fields):
        total = defaultdict(lambda: 0)
        count_fields = [
            'impressions',
            'clicks',
            'gross_clicks',
            'unique_clicks',
            'conversions',
            'revenue',
            'profit',
            'cost',
            'sales'
        ]

        if fields:
            fields_dict = dict(
                impressions=1,
                clicks=1,
                conversions=1,
                revenue=1,
                cost=1
            )
            [fields_dict.update({field: 1}) for field, value in fields.items() if value]

        count_fields = [fd for fd in count_fields if fd in fields_dict]

        for doc in datas:
            for fd in count_fields:
                total[fd] += doc.get(fd, 0)

        result = cls.create_calculate_result(fields_dict, [total])
        return result

    @classmethod
    def CTR(cls, result):
        """
            Click-Through-Rate
        """
        clicks, impressions = result.get('clicks', 0), result.get('impressions')
        return '%0.2f' % (clicks / impressions * 100) if impressions else '*'

    @classmethod
    def CPC(cls, result):
        """
            Cost Per Click
        """
        cost, clicks = result.get('cost', 0), result.get('clicks')
        return '%0.2f' % (cost / clicks) if clicks else '*'

    @classmethod
    def CPM(cls, result):
        """
            Cost Per Thousand Impression
        """
        cost, impressions = result.get('cost', 0), result.get('impressions')
        return '%0.2f' % (cost / impressions * 1000) if impressions else '*'

    @classmethod
    def CR(cls, result):
        """
            Cost Per Thousand Impression
        """
        conversions, clicks = result.get('conversions', 0), result.get('clicks')
        return '%0.2f' % (conversions / clicks * 100) if clicks else '*'

    @classmethod
    def CPA(cls, result):
        """
            Cost Per conversion
        """
        cost, conversions = result.get('cost', 0), result.get('conversions')
        return '%0.2f' % (cost / conversions) if conversions else '*'

    @classmethod
    def RPM(cls, result):
        """
            Revenue Per Thousand Impression
        """
        revenue, impressions = result.get('revenue', 0), result.get('impressions')
        return '%0.2f' % (revenue / impressions * 1000) if impressions else '*'

    @classmethod
    def RPC(cls, result):
        """
            Revenue Per Thousand Impression
        """
        revenue, clicks = result.get('revenue', 0), result.get('clicks')
        return '%0.2f' % (revenue / clicks * 100) if clicks else '*'

    @classmethod
    def RPA(cls, result):
        """
            Revenue Per conversion
        """
        revenue, conversions = result.get('revenue', 0), result.get('conversions')
        return '%0.2f' % (revenue / conversions) if conversions else '*'

    @classmethod
    def EPC(cls, result):
        """
            cost Per hundred conversion
        """
        cost, clicks = result.get('cost', 0), result.get('clicks')
        return '%0.2f' % (cost / clicks * 100) if clicks else '*'

if __name__ == '__main__':
    pass
