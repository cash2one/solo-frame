# coding=utf-8
from enum import Enum
from solo.web.mongo import Doc
from app.leadhug.controller.tools import Tool, DateTime
from datetime import datetime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey


class InvoiceFrequency(Enum):
    day = 'day'
    week = 'week'
    month = 'month'
    year = 'year'


class Affiliate(Doc):
    structure = dict(
        _id=int,
        user_id=int,
        country=str,
        status=str,          # 0 deleted; 1 active; 2 pending;
        account_manager=int,
        company=str,
        create_time=str,
        last_update=str,
        payment={
            'invoice_frequency': int,
            'threshold': float,
            'payment_method': str,
            'beneficiary': str,
            'account_number': str,
            'bank': str,
            'route': str,
            'paypal': str
        }
    )

    _t = DateTime()

    default_values = {
        'payment': {
            'invoice_frequency': '',
            'threshold': '',
            'payment_method': '',
            'beneficiary': '',
            'account_number': '',
            'bank': '',
            'route': '',
            'paypal': ''
        }
    }

    @classmethod
    def _save(cls, **kw):
        aff = Affiliate(dict(
            _id=_gid(GidKey.affiliate_key),
            user_id=int(kw.get('user_id')),
            country=kw.get('country'),
            account_manager=int(kw.get('account_manager')) if kw.get('account_manager') else None,
            company=kw.get('company'),
            status=kw.get('status', '1'),
            create_time=cls._t.today,
            last_update=cls._t.today,
            payment=kw.get('payment')
        ), True)
        aff.save()
        return aff

    @classmethod
    def _update(cls, aff_id, **kwargs):
        now = datetime.now()
        last_update = Tool.datetime_str(now, "%Y%m%d-%H:%M:%S")
        aff = cls.find_one(dict(_id=int(aff_id)))
        aff._id = int(aff_id)
        aff.country = kwargs['country']
        if kwargs.get('account_manager'):
            aff.account_manager = int(kwargs['account_manager'])
        aff.company = kwargs['company']
        aff.status = kwargs.get('status')
        aff.last_update = last_update
        aff.payment = kwargs.get('payment')
        aff.save()
