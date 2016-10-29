# coding=utf-8
from __future__ import division
from collections import OrderedDict, defaultdict
from bson import SON
from bson.code import Code
from pymongo.errors import OperationFailure
from solo.config import MONGO_CONFIG
from mongokit import Connection


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
        offers = kw.get('offers_id')
        api_offer_name = fields.get('api_offer_name')
        offer_name = fields.get('offer_name')
        if offer_name:
            condition.update(dict(offer_id={"$lt": 1000000}))
            if offers:
                condition.update(dict(offer_id={"$in": [int(i) for i in offers]}))
        elif api_offer_name:
            condition.update(dict(offer_id={"$gte": 1000000}))

        condition.update({
            'day': {
                '$gte': start.strip(),
                '$lte': end.strip()
            }
        })

        collection = cls.db.reportHour if cls.__name__ == 'ReportHour' else cls.db.reportDay

        # total_count, results = cls.get_map_reduce_result(collection, fields_dict, condition)
        # total_count, results = cls.get_group_result(collection, fields_dict, condition)
        total_count, results = cls.get_aggregate_result(collection, fields_dict, condition, limit, skip)

        calculate_result = cls.create_calculate_result(fields_dict, results) if results != False else False
        return calculate_result, total_count

    # map_reduce start
    @classmethod
    def get_map_reduce_result(cls, collection, fields_dict, condition):
        initial = cls.create_initial(fields_dict)
        groups = cls.create_group(fields_dict)
        _map = cls.map_fun(groups, initial)
        _reduce = cls.reduce_fun(initial)
        results = cls.result(collection, _map, _reduce, condition)
        return len(results), results

    @classmethod
    def map_fun(cls, groups, initial):
        '''
            function(){
                emit(keys, values);
            }
        '''

        keys = '{'
        for key in groups.keys():
            keys += '{key}: this.{key},'.format(key=key)
        keys += '}'

        values = '{'
        for v in initial.keys():
            values += '{v}: this.{v},'.format(v=v)
        values += '}'

        _map = '''function(){
            emit(%s, %s)
        }''' % (keys, values)
        return Code(_map)

    @classmethod
    def reduce_fun(cls, initial):
        '''
            function(key, values){
                for(var i=0; i<values.length; i++){
                    each(initial, function(key, value){
                        initial[key] += values[i][key]
                    })
                }
                return initial
            }
        '''
        res = dict()
        for k in initial.keys():
            res[k] = 0

        _reduce = '''
            function(key, values){
                var res = %s;
                var res_list = %s;
                for(var i=0; i<values.length; i++){
                    for(var j=0; j<res_list.length; j++){
                        res[res_list[j]] += values[i][res_list[j]]
                    }
                }
                return res
            }
        ''' % (res, res.keys())
        return Code(_reduce)

    @classmethod
    def result(cls, collection,  _map, _reduce, condition):
        res = collection.inline_map_reduce(_map, _reduce, full_response=False, query=condition)
        result = []
        for doc in res:
            group_fields = doc.get('_id')
            values = doc.get('value')
            values.update(group_fields)
            result.append(values)
        return result
    # map_reduce end

    # group method start
    @classmethod
    def get_group_result(cls, collection, fields_dict, condition):
        initial = cls.create_initial(fields_dict)
        groups = cls.create_group(fields_dict)
        reducer = cls.create_reducer(initial)
        results = collection.group(key=groups, condition=condition, initial=initial, reduce=reducer, finalize=None)
        total_count = len(results)
        return total_count, results

    @classmethod
    def create_reducer(cls, initial):
        prev_str = ''
        for k, v in initial.items():
            prev_str += 'prev.{k} += obj.{k};'.format(k=k)

        reduce_code = 'function(obj, prev){%s}' % prev_str
        return Code(reduce_code)
    # group method end

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

        countries = kw.get('countries')
        if countries:
            spec.update(dict(country={"$in": countries}))

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
        groups = OrderedDict()
        [groups.update({fd: 1}) for fd in group_fields if fd in fields_dict]
        return groups

    # aggregate start
    @classmethod
    def get_aggregate_result(cls, collection, fields_dict, match, limit, skip):
        sum_field = cls.create_sum_field(fields_dict)
        groups2 = cls.create_aggregate_groups(fields_dict, sum_field)
        try:
            res = collection.aggregate([
                {"$match": match},
                {"$group": groups2},
                {"$sort": SON([("_id", 1)])},
            ])
        except OperationFailure:
            return 0, False
        result = res.get('result')
        for r in result:
            fields = r.get('_id')
            r.pop('_id')
            r.update(fields)
        return len(result), result

    @classmethod
    def create_sum_field(cls, field_dict):
        fields = [
            'gross_clicks',
            'unique_clicks',
            'revenue',
            'profit',
            'sales'
        ]

        sum_field = dict(
            impressions={"$sum": "$impressions"},
            clicks={"$sum": "$clicks"},
            cost={"$sum": "$cost"},
            conversions={"$sum": "$conversions"},
        )
        [sum_field.update({fd: {"$sum": "${}".format(fd)}}) for fd in fields if fd in field_dict]
        return sum_field

    @classmethod
    def create_aggregate_groups(cls, fields_dict, sum_field):
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
            'category_status',
            'hour',
            'day',
            'week',
            'month',
            'year'
        ]
        groups = {'_id': {}}
        [groups['_id'].update({fd: "${}".format(fd)}) for fd in group_fields if fd in fields_dict]
        if 'offer_name' in fields_dict:
            groups['_id'].update({'offer_id': "$offer_id"})
        if 'affiliate_name' in fields_dict:
            groups['_id'].update({'affiliate_id': "$affiliate_id"})
        if 'advertiser_name' in fields_dict:
            groups['_id'].update({'advertiser_id': "$advertiser_id"})
        if 'api_offer_name' in fields_dict:
            groups['_id'].update({'offer_name': "$offer_name"})
        groups.update(sum_field)
        return groups
    # aggregate end

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

        def result_update(r):
            for fd in calculate:
                res = getattr(cls, fd)(r)
                r.update({fd: res})
            return r

        results = map(result_update, results)

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
                # revenue=1,
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

