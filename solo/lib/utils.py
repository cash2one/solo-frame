#!/usr/bin/env python
# coding:utf-8
import datetime
import _env  # noqa
import re
import time
import os
import pytz


def is_email(email):
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match(rule, email)
    if match:
        return True
    return False


def is_valid_password(password):
    """
    检测密码
    :param password:
    :return:
    """
    pattern = re.compile(r'^[\@A-Za-z0-9\!\#\$\^\&\*\.\~]{6,22}$')
    match = pattern.match(password)
    if not match:
        return False
    return True


def is_valid_name(name, min_length=6, max_length=12):
    '''检查用户名是否合法.

    只包含字母,数字和下划线, 默认长度大于等于6小于等于12
    '''
    if re.match("^[a-zA-Z0-9_]+$", name) and \
            min_length <= len(name) <= max_length:
        return True
    return False


def time13():
    '''返回13位整型时间戳.
    '''
    return int(time.time() * 1000)


def time13_to_cts(timestamp):
    dt = datetime.datetime.fromtimestamp(
        timestamp / 1000,
        pytz.timezone('Asia/Shanghai'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def is_valid_path(path):
    if re.match("^[a-zA-Z0-9_\/]+$", path):
        return True
    return False


class DateTime():
    date_format = '%Y-%m-%d'
    time_format = '%Y-%m-%d %H:%M:%S'
    current_time = datetime.datetime.now().strftime(time_format)
    today = datetime.date.today().strftime(date_format)

    @classmethod
    def get_day(cls, days):
        return (datetime.date.today() - datetime.timedelta(days=int(days))
                ).strftime(cls.date_format)


def load_env_config(name, default=None):
    if name in os.environ:
        return os.getenv(name, default)
    return default
