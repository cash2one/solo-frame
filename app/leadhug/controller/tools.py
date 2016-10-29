# coding=utf-8
import _env  # noqa
import datetime

class Tool(object):

    date_format = '%Y-%m-%d'

    @staticmethod
    def datetime_str(date, format):
        return datetime.datetime.strftime(date, format)

    @staticmethod
    def str_datetime(date, format):
        return datetime.datetime.strptime(date, format)


class DateTime():

    date_format = '%Y-%m-%d'
    time_format = '%Y-%m-%d %H:%M:%S'

    @property
    def current_time(self):
        return datetime.datetime.now().strftime(DateTime.time_format)

    @property
    def today(self):
        return datetime.date.today().strftime(DateTime.date_format)

    @classmethod
    def get_day(cls, days):
        return (datetime.date.today() - datetime.timedelta(days=int(days))).strftime(cls.date_format)

    @classmethod
    def get_day_date(cls, days):
        return datetime.date.today() - datetime.timedelta(days=int(days))
