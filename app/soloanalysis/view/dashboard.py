# coding:utf-8

from _route import route
from app.soloanalysis.model.activity import Activity
from app.soloanalysis.view._base import View, JsonView
#from solo.web.view import View
from app.soloanalysis.model.publisher import Publisher
from app.soloanalysis.model.slot import Slot
from yajl import loads,dumps
import csv


@route('/')
class index(View):
    def get(self):
        self.redirect('/dashboard')


@route('/dashboard')
class Dashboard(View):

    def get(self):
        publisher = Publisher.find()
        self.render(publisher=publisher)


@route('/j/dashboard')
class Filter(JsonView):

    def post(self):
        sort_by_time,sort_by_country = Activity.time_country(self)
        self.render(dumps({'sort_by_time': sort_by_time, 'sort_by_country': sort_by_country}))


@route('/j/get_slot')
class GetSlot(JsonView):
    def get(self):
        publisher_id = self.get_argument('publisher_id')
        slot = Publisher.find_one(dict(publisher_id=int(publisher_id)))
        self.render(slot)


@route('/j/charts')
class GetCharts(JsonView):
    """{
        'new': {
            'x':[]
            'y':[]
        },
        'active': {
            'x':[]
            'y':[]
        },
        'total': {
            'x':[]
            'y':[]
        }
    }
    """
    def post(self):
        result = Activity.get_chart(self)
        self.render(result)


@route('/j/export/time')
class Export(View):
    def get(self):
        fieldnames = ['date', 'new', 'active', 'total']
        data, _ = Activity.export_time_country(self)
        for item in data:
            item['date'] = item['_id']
            del item['_id']
        with open('date_report.csv', 'wb') as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        fd = open('date_report.csv', 'r')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=date_report.csv')
        self.write(fd.read())
        self.finish()


@route('/j/export/country')
class Export(View):
    def get(self):
        fieldnames = ['country', 'new', 'active', 'total']
        _, data = Activity.export_time_country(self)
        for item in data:
            item['country'] = item['_id']
            del item['_id']
        with open('country_report.csv', 'wb') as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        fd = open('country_report.csv', 'r')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=country_report.csv')
        self.write(fd.read())
        self.finish()
