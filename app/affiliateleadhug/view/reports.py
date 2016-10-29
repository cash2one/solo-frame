# coding:utf-8
import csv
from json import loads
from concurrent.futures import ThreadPoolExecutor
import tornado
from tornado.concurrent import run_on_executor
from _route import route
from _base import View, JsonLoginView, LoginView
from app.leadhug.model.country import Country as _c
from app.leadhug.model.offer_affiliate import OfferAffiliate
from app.leadhug.model.offers import Offers
from app.leadhug.model.report_day import ReportDay
from app.leadhug.model.report_hour import ReportHour


@route('/report')
class Report(LoginView):

    def get(self):
        affiliate_id = self.current_user_id
        off_affs = OfferAffiliate._query(affiliate_id=affiliate_id)
        offer_ids = [off_aff.offer_id for off_aff in off_affs]
        offers = Offers.find(dict(_id={'$in': offer_ids}))
        self.render(
            countries=_c().countries,
            offers=offers
        )


@route('/countries')
class Country(JsonLoginView):

    def get(self):
        self.finish(dict(countries=_c().countries))


@route('/j/report')
class ReportDate(JsonLoginView):

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        user = self.current_user
        start = self.json.start
        end = self.json.end
        query_fields = self.json.fields
        payout_range = self.json.payout_range
        selected_filter = self.json.filter or {}
        selected_filter['affiliates_name'].append(user._id)
        payout_is_zero = self.json.payout_is_zero
        limit = int(self.json.limit)
        page = int(self.json.page)
        hour = query_fields.get('hour')
        obj = ReportHour() if hour else ReportDay()

        data, data_count, total = yield self.get_result(obj, start, end, query_fields, payout_is_zero, payout_range, limit, page, selected_filter)

        self.finish(dict(docs=data, doc_count=data_count, total=total[0]))

    @run_on_executor
    def get_result(self, obj, start, end, query_fields, payout_is_zero, payout_range, limit, page, selected_filter):
        data, total_count = obj.__class__.get_range_data(
            start, end, fields=query_fields, **selected_filter)

        if isinstance(data, bool) and not data:
            return False, 0, [0]

        data = sorted(data, key=lambda d: d['day'], reverse=False)

        min, mix = payout_range.get('min', 0), payout_range.get('mix', 10000)
        for doc in data:
            payout = doc.get('cost')
            data = filter(lambda doc: float(min) <= payout <= float(mix), data)

        if not payout_is_zero:
            data = filter(lambda doc: doc.get('cost') != 0, data)

        data_count = len(data)
        data = data[limit * (page - 1): limit * page]
        total = obj.__class__.total(data, query_fields)

        return data, data_count, total


@route("/j/export_report")
class ReportExport(LoginView):

    executor = ThreadPoolExecutor(5)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        cookie = self.get_cookie('S')
        user = self.current_user
        query_fields = loads(self.get_argument('fields'))
        selected_filter = loads(self.get_argument('filter'))
        selected_filter['affiliates_name'].append(user._id)
        payout_is_zero = loads(self.get_argument('payout_is_zero'))
        payout_range = loads(self.get_argument('payout_range'))
        start = selected_filter.get('time_range').get('start')
        end = selected_filter.get('time_range').get('end')
        hour = query_fields.get('hour')
        obj = ReportHour() if hour else ReportDay()

        data, data_count, total = yield self.get_result(obj, start, end, query_fields, payout_is_zero, payout_range, selected_filter)

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
            [fieldnames.append(i)
             for i in init_fieldnames if i not in fieldnames]

            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            dict_writer.writerow(total)

        _file = file(_file_name, 'r')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header(
            'Content-Disposition', 'attachment; filename=report.csv')
        self.write(_file.read())
        self.finish()

    @run_on_executor
    def get_result(self, obj, start, end, query_fields, payout_is_zero, payout_range, selected_filter):
        data, total_count = obj.__class__.get_range_data(
            start, end, fields=query_fields, **selected_filter)

        if isinstance(data, bool) and not data:
            return False, 0, [0]

        min, mix = payout_range.get('min', 0), payout_range.get('mix', 10000)
        for doc in data:
            payout = doc.get('cost')
            data = filter(lambda doc: float(min) <= payout <= float(mix), data)

        if not payout_is_zero:
            data = filter(lambda doc: doc.get('cost') != 0, data)

        for field, value in query_fields.items():
            if not value:
                query_fields.pop(field)

        total = obj.__class__.total(data, query_fields)[0]

        return data, total_count, total
