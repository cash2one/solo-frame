# coding=utf-8
from __future__ import division
from collections import OrderedDict, defaultdict
from solo.config import MONGO_CONFIG, DBNAME
from mongokit import Connection
from app.new_pingstart.view.country import Country as _c
from app.new_pingstart.model.slots import Slots


class ReportInterFace(object):

    db = Connection(MONGO_CONFIG.get('host'))[DBNAME]

    @classmethod
    def model_name(cls):
        return cls.__name__

    @classmethod
    def get_network_data(cls, day, slots=None, networks=None):
        # OverView
        collection = cls.db.dateReport if cls.model_name() == 'CallableDateReport' else cls.db.countryReport
        groups = dict(_id={'network': "$network"})
        sum_field = cls.create_sum_field()
        groups.update(sum_field)
        match = dict(network={"$in": networks or []}, slot_id={"$in": slots or []}, createdTime=day.strip())
        aggregate_condition = [
            {"$match": match},
            {"$group": groups},
            {"$sort": {"_id": 1}},
        ]
        res = collection.aggregate(aggregate_condition)

        result = res.get('result')
        for r in result:
            fields = r.get('_id')
            r.pop('_id')
            r.update(fields)
            show_revenue = r.get('show_revenue')
            if show_revenue:
                r['show_revenue'] = show_revenue / 10000

        calculate_result = cls.create_calculate_result(result)
        return calculate_result

    @classmethod
    def get_slot_data(cls, start=None, end=None, slots=None, networks=None, date_or_country=None):

        collection = cls.db.countryReport if cls.model_name() == 'CallableCountryReport' else cls.db.dateReport
        sum_field = cls.create_sum_field()
        # Stats
        match = dict(
            createdTime={
                '$gte': start.strip(),
                '$lte': end.strip()
            },

            slot_id={"$in": slots or []},
            network={"$in": networks or []}
        )

        if date_or_country == 'date':
            groups = dict(
                _id={
                    'createdTime': '$createdTime',
                }
            )
        elif date_or_country == 'country':
            groups = dict(
                _id={
                    'country': '$country',
                }
            )
        else:
            groups = dict(
                _id={
                    'slot_id': '$slot_id',
                }
            )

        groups.update(sum_field)
        res = collection.aggregate([
            {"$match": match},
            {"$group": groups},
            {"$sort": {'createdTime': -1}},
        ])

        result = res.get('result')

        if date_or_country not in ['date', 'country']:
            for r in result:
                fields = r.get('_id')
                r.pop('_id')
                r.update(fields)
                show_revenue = r.get('show_revenue')
                if show_revenue:
                    r['show_revenue'] = show_revenue / 10000
                r['name'] = Slots.find_one(dict(_id=r['slot_id'])).name
        else:
            for r in result:
                fields = r.get('_id')
                r.pop('_id')
                r.update(fields)
                show_revenue = r.get('show_revenue')
                if show_revenue:
                    r['show_revenue'] = show_revenue / 10000

        calculate_result = cls.create_calculate_result(result)

        return calculate_result

    @classmethod
    def get_network_slot_data(cls, start=None, end=None, slots=None, networks=None, content=None, report_obj=None, need_fields=None):

        collection = cls.db.countryReport if cls.model_name() == 'CallableCountryReport' else cls.db.dateReport
        sum_field = cls.create_sum_field()
        # Stats
        V = []
        for network in networks:
            match = dict(
                createdTime={
                    '$gte': start.strip(),
                    '$lte': end.strip()
                },

                slot_id={"$in": slots or []},
                network=network
            )

            if content.date_or_country == 'date':
                groups = dict(
                    _id={
                        'createdTime': '$createdTime',
                    }
                )
            elif content.date_or_country == 'country':
                groups = dict(
                    _id={
                        'country': '$country',
                    }
                )
            else:
                groups = dict(
                    _id={
                        'slot_id': '$slot_id',
                    }
                )

            groups.update(sum_field)
            res = collection.aggregate([
                {"$match": match},
                {"$group": groups},
                {"$sort": {'createdTime': -1}},
            ])

            result = res.get('result')
            if content.date_or_country not in ['date', 'country']:
                for r in result:
                    fields = r.get('_id')
                    r.pop('_id')
                    r.update(fields)
                    show_revenue = r.get('show_revenue')
                    if show_revenue:
                        r['show_revenue'] = show_revenue / 10000
                    r['name'] = Slots.find_one(dict(_id=r['slot_id'])).name
            else:
                for r in result:
                    fields = r.get('_id')
                    r.pop('_id')
                    r.update(fields)
                    show_revenue = r.get('show_revenue')
                    if show_revenue:
                        r['show_revenue'] = show_revenue / 10000

            calculate_result = cls.create_calculate_result(result)
            if calculate_result:
                if content.date_or_country == 'country':
                    for doc in calculate_result:
                        _country = doc.get('country')
                        if _country:
                            doc['full_country'] = _c.info.get(_country.upper())
                if content.date_or_country == 'date':
                    calculate_result = sorted(calculate_result, key=lambda d: d['createdTime'], reverse=True)
                elif content.date_or_country == 'country':
                    calculate_result = sorted(calculate_result, key=lambda d: d['show_revenue'], reverse=True)
                else:
                    calculate_result = sorted(calculate_result, key=lambda d: d['slot_id'], reverse=True)
                total_datas = report_obj.total(calculate_result, content.date_or_country)[0]
            else:
                total_datas = dict()
                for f in need_fields:
                    total_datas[f] = '*'
            V.append({network: [calculate_result, total_datas]})
        return V

    @classmethod
    def get_slot_highchart_data(cls, day, slots=None, networks=None):

        collection = cls.db.dateReport

        sum_field = cls.create_sum_field()
        # Stats
        match = dict(
            createdTime=day,

            slot_id={"$in": slots or []},
            network={"$in": networks or []}
        )

        groups = dict(
            _id={
                'network': '$network'
            }
        )
        groups.update(sum_field)
        res = collection.aggregate([
            {"$match": match},
            {"$group": groups},
            {"$sort": {'createdTime': -1}},
        ])

        result = res.get('result')
        for r in result:
            fields = r.get('_id')
            r.pop('_id')
            r.update(fields)
            show_revenue = r.get('show_revenue')
            if show_revenue:
                r['show_revenue'] = show_revenue / 10000

        calculate_result = cls.create_calculate_result(result)

        return calculate_result

    @classmethod
    def create_calculate_result(cls, results):
        calculate_fields = [
            'CPC',
            'eCPM',
            'CTR',
            'FillRate'
        ]
        calculate = [fd for fd in calculate_fields]

        def result_upate(r):
            for fd in calculate:
                res = getattr(cls, fd)(r)
                r.update({fd: res})
            return r

        results = map(result_upate, results)

        return results

    @classmethod
    def create_sum_field(cls):
        fields = [
            'impression',
            'show_click',
            'show_conversion',
            'show_revenue',
            'fill',
            'request'
        ]

        sum_field = {}
        [sum_field.update({fd: {"$sum": "${}".format(fd)}}) for fd in fields]
        return sum_field

    @classmethod
    def total(cls, datas, name=None):
        total = defaultdict(lambda: 0)
        count_fields = [
            'impression',
            'show_click',
            'show_conversion',
            'show_revenue',
            'fill',
            'request',
        ]

        for doc in datas:
            for fd in count_fields:
                total[fd] += doc.get(fd, 0)
        if name not in ['date', 'country']:
            total['name'] = '*'

        result = cls.create_calculate_result([total])
        return result

    @classmethod
    def CTR(cls, result):
        """
            Click-Through-Rate
        """
        clicks, impressions = result.get('show_click', 0), result.get('impression')
        return '%0.2f' % (clicks / impressions * 100) if impressions else '*'

    @classmethod
    def CPC(cls, result):
        """
            Cost Per Click
        """
        cost, clicks = result.get('show_revenue', 0), result.get('show_click')
        return '%0.2f' % (cost / clicks) if clicks else '*'

    @classmethod
    def eCPM(cls, result):
        """
            Cost Per Thousand Impression
        """
        cost, impressions = result.get('show_revenue', 0), result.get('impression')
        return '%0.2f' % (cost / impressions * 1000) if impressions else '*'

    @classmethod
    def FillRate(cls, result):
        """
            cost Per hundred conversion
        """
        request, fill = result.get('request', 0), result.get('fill', 0)
        return '%0.2f' % (fill / request * 100) if request else '*'


if __name__ == '__main__':
    pass
