#!/usr/bin/env python
# coding:utf-8
import datetime
import time

"""
注意, 这里所有的时间都是UTC时间
"""

__author__ = 'Mush Mo'

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def tomorrow():
    """返回下一个自然日0时0分的时间戳
    """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return int(time.mktime(tomorrow.timetuple()))


def today():
    """返回今天0时0分的时间戳
    """
    today = datetime.date.today()
    return int(time.mktime(today.timetuple()))


if __name__ == '__main__':
    print today() - tomorrow()
