# coding=utf-8
from __future__ import division
from collections import OrderedDict
from decimal import Decimal
import _env  # noqa
from solo.web.mongo import Doc
from app.new_pingstart.controller.report_interface import ReportInterFace


class CountryReport(Doc, ReportInterFace):

    structure = dict(
        _id=int,
        impression=int,
        conversion=int,
        show_conversion=int,
        revenue=float,
        show_revenue=float,
        slot_id=int,
        country=str,
        network=str,
        request=int,
        fill=float,
        click=int,
        show_click=int,
        createdTime=str,
    )

    default_values = dict(
        revenue=100,
        network='PingStart',
        request=100,
        click=100,
        fill=0
    )

if __name__ == '__main__':

    r = CountryReport(dict(
        _id=3,
        impression=10,
        conversion=10,
        show_conversion=9,
        show_revenue=9,
        country='india',
        slot_id=19,
        show_click=99,
        createdTime='2016-05-31'
    ), True).save()
