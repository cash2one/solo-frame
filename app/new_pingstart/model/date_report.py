# coding=utf-8
from __future__ import division
from collections import OrderedDict
from decimal import Decimal
import _env  # noqa
from solo.web.mongo import Doc
from app.new_pingstart.controller.report_interface import ReportInterFace


class DateReport(Doc, ReportInterFace):

    structure = dict(
        _id=int,
        impression=int,
        conversion=int,
        show_conversion=int,
        revenue=float,
        show_revenue=float,
        slot_id=int,
        network=str,
        request=int,
        fill=float,
        click=int,
        show_click=int,
        createdTime=str,
    )

    default_values = dict(
        revenue=100,
        request=100,
        click=100,
        fill=0
    )


if __name__ == '__main__':

    r = DateReport(dict(
        _id=7,
        network='MoPub',
        impression=200,
        conversion=200,
        show_conversion=200,
        show_revenue=200,
        slot_id=20,
        show_click=200,
        createdTime='2016-05-31'
    ), True).save()
