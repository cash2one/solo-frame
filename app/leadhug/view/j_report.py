# coding=utf-8
import csv
from json import loads
import os
from concurrent.futures import ThreadPoolExecutor
import tornado
from tornado.concurrent import run_on_executor
import _env  # noqa
from _route import route
from app.leadhug.model.advertisers import Advertisers
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.category import Category
from app.leadhug.model.offers import Offers
from app.leadhug.model.role import Role
from app.leadhug.model.user import User
from app.leadhug.view._base import JsonErrView, JsonLoginView, LoginView
from app.leadhug.model.report_day import ReportDay
from app.leadhug.model.report_hour import ReportHour


@route("/j/report")
class Report(JsonLoginView):
    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start = self.json.start
        end = self.json.end
        query_fields = self.json.query_fields
        selected_filter = self.json.selected_filter or {}
        ams = selected_filter.get('ams_id', None)
        bds = selected_filter.get('bds_id', None)
        if ams:
            affiliates = Affiliate.find(dict(account_manager={"$in": [int(am_id) for am_id in ams]}))
            for aff in affiliates:
                selected_filter['affiliates_name'].append(aff.user_id)

        if bds:
            advertisers = Advertisers.find(dict(account_manager={"$in": [int(bd_id) for bd_id in bds]}))
            for ad in advertisers:
                selected_filter['advertisers_name'].append(ad.user_id)
        conversions_is_zero = self.json.conversions_is_zero
        limit = int(self.json.limit)
        page = int(self.json.page)
        hour = query_fields.get('hour')
        obj = ReportHour() if hour else ReportDay()

        data, data_count, total = yield self.get_data(obj, start, end, query_fields, limit, page, selected_filter, conversions_is_zero)

        self.finish(dict(docs=data, doc_count=data_count, total=total[0]))

    @run_on_executor
    def get_data(self, obj, start, end, query_fields, limit, page, selected_filter, conversions_is_zero):
        data, data_count = obj.__class__.get_range_data(
            start,
            end,
            fields=query_fields,
            limit=limit,
            skip=limit * (page - 1),
            **selected_filter
        )

        if isinstance(data, bool) and not data:
            return False, 0, [0]
        data = sorted(data, key=lambda d: d['day'] if d.get('day') else '', reverse=False)
        data = data[limit * (page - 1): limit * page]

        if not conversions_is_zero:
            data = filter(lambda doc: doc.get('cost') != 0, data)

        total = obj.__class__.total(data, query_fields)

        if query_fields.get('affiliate_name') or query_fields.get('advertisers_name'):
            def display_am(doc):
                if doc.get('affiliate_name'):
                    affiliate_id = doc.get('affiliate_id')
                    doc['AM'] = ''
                    if affiliate_id:
                        affiliate = Affiliate.find_one(dict(user_id=int(affiliate_id)))
                        if affiliate and affiliate.account_manager:
                            am = User.find_one(dict(_id=int(affiliate.account_manager)))
                            doc['AM'] = am.account
                if doc.get('advertisers_name'):
                    advertiser_id = doc.get('advertiser_id')
                    doc['BD'] = ''
                    if advertiser_id:
                        advertiser = Advertisers.find_one(dict(user_id=int(advertiser_id)))
                        if advertiser and advertiser.account_manager:
                            bd = User.find_one(dict(_id=int(advertiser.account_manager)))
                            doc['BD'] = bd.account
                return doc
            data = map(display_am, data)
        return data, data_count, total


@route("/j/export_report")
class ReportExport(LoginView):

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        cookie = self.get_cookie('S')
        query_fields = loads(self.get_argument('fields'))
        selected_filter = loads(self.get_argument('filter'))
        ams = selected_filter.get('ams_id', None)
        bds = selected_filter.get('bds_id', None)
        if ams:
            affiliates = Affiliate.find(dict(account_manager={"$in": [int(am_id) for am_id in ams]}))
            for aff in affiliates:
                selected_filter['affiliates_name'].append(aff.user_id)

        if bds:
            advertisers = Advertisers.find(dict(account_manager={"$in": [int(bd_id) for bd_id in bds]}))
            for ad in advertisers:
                selected_filter['advertisers_name'].append(ad.user_id)
        payout_is_zero = loads(self.get_argument('payout_is_zero'))
        time_range = loads(self.get_argument('time_range'))
        start = time_range.get('start')
        end = time_range.get('end')
        hour = query_fields.get('hour')
        obj = ReportHour() if hour else ReportDay()
        data, data_count, total = yield self.get_result(obj, start, end, query_fields, payout_is_zero, selected_filter)

        if isinstance(data, bool) and not data:
            self.write(u'The result exceeds maximum size!')
            self.finish()
            return

        _file_name = '{}_report.csv'.format(cookie)
        with open(_file_name, 'wb') as f:
            init_fieldnames = ['impressions', 'clicks', 'cost', 'conversions']
            fieldnames = [k.decode('utf-8') for k in query_fields.keys()]
            for i in ['hour', 'day', 'week', 'month', 'year']:
                if i in fieldnames:
                    fieldnames.remove(i)
                    fieldnames.insert(0, i)

            if 'affiliate_name' in fieldnames:
                fieldnames.extend(['affiliate_id', 'AM'])

            if 'advertiser_name' in fieldnames:
                fieldnames.extend(['advertiser_id', 'BD'])

            [fieldnames.append(i) for i in init_fieldnames if i not in fieldnames]

            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            dict_writer.writerow(total)

        _file = file(_file_name, 'r')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=report.csv')
        self.write(_file.read())
        self.finish()

    @run_on_executor
    def get_result(self, obj, start, end, query_fields, payout_is_zero, selected_filter):

        data, data_count = obj.__class__.get_range_data(start, end, fields=query_fields, **selected_filter)
        if isinstance(data, bool) and not data:
            return False, 0, [0]

        if not payout_is_zero:
            data = filter(lambda doc: doc.get('cost') != 0, data)

        for field, value in query_fields.items():
            if not value:
                query_fields.pop(field)

        total = obj.__class__.total(data, query_fields)[0]

        if query_fields.get('affiliate_name') or query_fields.get('advertisers_name'):
            def display_am(doc):
                if doc.get('affiliate_name'):
                    affiliate_id = doc.get('affiliate_id')
                    doc['AM'] = ''
                    if affiliate_id:
                        affiliate = Affiliate.find_one(dict(user_id=int(affiliate_id)))
                        if affiliate and affiliate.account_manager:
                            am = User.find_one(dict(_id=int(affiliate.account_manager)))
                            doc['AM'] = am.account
                if doc.get('advertisers_name'):
                    advertiser_id = doc.get('advertiser_id')
                    doc['BD'] = ''
                    if advertiser_id:
                        advertiser = Advertisers.find_one(dict(user_id=int(advertiser_id)))
                        if advertiser and advertiser.account_manager:
                            bd = User.find_one(dict(_id=int(advertiser.account_manager)))
                            doc['BD'] = bd.account
                return doc
            data = map(display_am, data)

        return data, data_count, total


@route('/j/report/filters')
class ReportOffers(JsonLoginView):

    def get(self):
        offer_spce = dict(status={"$ne": 0}, is_api={"$ne": True})
        offers = Offers.find(offer_spce, dict(_id=1, title=1))

        affiliate_spec = dict(status={"$ne": 0})
        affiliates = Affiliate.find(affiliate_spec, dict(user_id=1))
        for aff in affiliates:
            user = User.find_one(dict(_id=int(aff.user_id)), dict(_id=1, account=1))
            if not user:
                continue
            aff['_id'] = user._id
            aff['name'] = user.account

        advertiser_spec = dict(status={"$ne": 0})
        advertisers = Advertisers.find(advertiser_spec, dict(user_id=1))
        for ad in advertisers:
            user = User.find_one(dict(_id=int(ad.user_id)), dict(_id=1, account=1))
            if not user:
                continue
            ad['_id'] = user._id
            ad['name'] = user.account

        categories = Category.find(dict(status={"$ne": 0}), dict(_id=1, name=1))

        ams = User.find(dict(role_id=Role.am()._id, deleted=False), dict(_id=1, account=1, role_id=1))
        ams = [am for am in ams if am.role_id and am._role == 'AM']
        bds = User.find(dict(role_id=Role.bd()._id, deleted=False), dict(_id=1, account=1, role_id=1))
        bds = [bd for bd in bds if bd.role_id and bd._role == 'BD']
        self.finish(dict(
            offers=offers,
            affiliates=affiliates,
            advertisers=advertisers,
            categories=categories,
            ams=ams,
            bds=bds
        ))




