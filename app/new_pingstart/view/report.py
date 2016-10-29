#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import LoginView, JsonLoginView
from app.new_pingstart.controller.tools import DateTime, Tool
from app.new_pingstart.model.country_report import CountryReport
from app.new_pingstart.model.date_report import DateReport
from app.new_pingstart.model.slots import Slots
from solo.lib.jsob import JsOb
from collections import defaultdict
from app.new_pingstart.view.country import Country as _c


@route("/report")
class Report(LoginView):

    def get(self):
        user_id = self.current_user_id
        slots = Slots.find(dict(appId=int(user_id), network={"$ne": []}, deleted=False))
        networks = set()
        for slot in slots:
            for net in slot.network:
                if net.get('is_auth'):
                    networks.add(net.get('network_name'))
        slot_ids = [int(s._id) for s in slots]

        yesterday = DateTime.get_day(1)
        overview_total_data = DateReport.get_network_data(yesterday, slots=slot_ids, networks=list(networks))
        total_data = defaultdict(lambda: 0)

        ps_data = ''
        for doc in overview_total_data:
            if doc.get('network') == 'PingStart':
                ps_data = doc
            total_data['impression'] += doc.get('impression', 0)
            total_data['show_revenue'] += doc.get('show_revenue', 0)
            total_data['show_conversion'] += doc.get('show_conversion', 0)
            total_data['show_click'] += doc.get('show_click', 0)

        if not total_data: total_data['show_revenue'] = '*'
        total_data['CPC'] = DateReport.CPC(total_data)
        total_data['eCPM'] = DateReport.eCPM(total_data)

        if ps_data:
            ps_data = DateReport.create_calculate_result([ps_data])[0]
        else:
            ps_data = dict(show_revenue='*', CPC='*', eCPM='*')

        self.render(slots=slots, overview_ps_data=ps_data, overview_total_data=total_data)


@route("/report/stats")
class Stats(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        content = self.json
        slots = Slots.find(dict(appId=int(user_id), network={"$ne": []}, deleted=False))
        networks = set()
        for slot in slots:
            for net in slot.network:
                if net.get('is_auth'):
                    networks.add(net.get('network_name'))

        networks = list(networks)
        slots = [int(content.slot)] if content.slot else [int(s._id) for s in slots]

        days = []
        days_data = {}
        if content.date_or_country == 'date':
            report_obj = DateReport
            need_fields = ['createdTime', 'impression', 'show_revenue', 'CPC', 'eCPM', 'CTR', 'FillRate', 'show_click', 'fill', 'request']
            start = Tool.str_datetime(content.start, Tool.date_format)
            end = Tool.str_datetime(content.end, Tool.date_format)
            for net in networks:
                days_data.setdefault(net, {})
            while start <= end:
                day = Tool.datetime_str(start, Tool.date_format)
                days.append(day)
                datas = report_obj.get_slot_highchart_data(day, slots, networks)
                self.result_data(datas, days_data)
                start = start + Tool.days(1)
        elif content.date_or_country == 'country':
            report_obj = CountryReport
            need_fields = ['country', 'impression', 'show_revenue', 'CPC', 'eCPM', 'CTR', 'FillRate', 'show_click', 'fill', 'request']
        else:
            report_obj = DateReport
            need_fields = ['slot', 'slot_name', 'impression', 'show_revenue', 'CPC', 'eCPM', 'CTR', 'FillRate', 'show_click', 'fill', 'request']
        detail_data = report_obj.get_slot_data(content.start, content.end, slots, networks, content.date_or_country)
        network_detail_data = report_obj.get_network_slot_data(content.start, content.end, slots, networks, content, report_obj, need_fields)
        if detail_data:
            if content.date_or_country == 'country':
                for doc in detail_data:
                    _country = doc.get('country')
                    if _country:
                        doc['full_country'] = _c.info.get(_country.upper())
            if content.date_or_country == 'date':
                detail_data = sorted(detail_data, key=lambda d: d['createdTime'], reverse=True)
            elif content.date_or_country == 'country':
                detail_data = sorted(detail_data, key=lambda d: d['show_revenue'], reverse=True)
            else:
                detail_data = sorted(detail_data, key=lambda d: d['slot_id'], reverse=True)
            total_datas = report_obj.total(detail_data, content.date_or_country)[0]
        else:
            total_datas = dict()
            for f in need_fields:
                total_datas[f] = '*'
        self.finish(dict(
            createdTime=days,
            table_data=detail_data,
            total_datas=total_datas,
            highchars_data=days_data,
            networks=networks,
            network_detail_data=network_detail_data
        ))

    def result_data(self, datas, days_data):

        datas_network = []
        for doc in datas:
            datas_network.append(doc.get('network'))

        for network in days_data.keys():
            days_data[network]['name'] = network
            for fd in ['impression', 'show_revenue', 'CPC', 'eCPM', 'CTR', 'FillRate', 'show_click', 'fill', 'request']:
                days_data[network].setdefault(fd, [])
                if datas:
                    for doc in datas:
                        if network == doc.get('network'):
                            fd_value = doc.get(fd, 0)

                            days_data[network][fd].append(float(fd_value) if fd_value != '*' else 0)
                        elif network not in datas_network:
                            days_data[network][fd].append(0)
                else:
                    days_data[network][fd].append(0)
        return days_data   

