# coding=utf-8
from collections import OrderedDict
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey
from app.leadhug.controller.invoice_interface import InterFace


CURRENCY_TYPES = ['U.S.$', 'RMB.￥']


class Invoice(Doc):

    structure = dict(
        _id=int,
        user_id=int,
        affiliate_id=int,
        time_range=dict(
            start=str,
            end=str
        ),
        _invoice=[dict(
            offer_id=int,
            actions=int,
            amount=float,
            real_pay=float,
            remark=str
        )],
        _invoice_number=str,
        currency=int,
        createdTime=str,
        last_update=str,
        deleted=bool,
        status=bool,  # 0:
    )

    _t = DateTime()

    indexes = [
        {'fields': ['_id']},
        {'fields': ['affiliate_id', 'deleted']},
    ]

    default_values = {
        'createdTime': _t.today,
        'last_update': _t.current_time,
        'deleted': False,
        'status': False
    }

    @classmethod
    def _create(cls, **kwargs):
        _id = _gid(GidKey.invoice_key)
        invoice = Invoice(dict(
            _id=_id,
            user_id=int(kwargs.get('user_id')),
            affiliate_id=int(kwargs.get('affiliate_id')),
            time_range=kwargs.get('time_range'),
            _invoice=kwargs.get('_invoices'),
            _invoice_number='newborn-{}'.format(_id),
            currency=kwargs.get('currency')
        ), True)
        invoice.save()

    @classmethod
    def _delete(cls, _id):
        invoice = cls._get(_id)
        invoice.deleted = True
        invoice.save()

    @classmethod
    def _get(cls, _id):
        return cls.find_one(dict(_id=int(_id)))

    @classmethod
    def _query(cls, spec, limit=10, offset=0):
        return cls.find(spec, limit=limit, skip=offset)

    @classmethod
    def _update(cls, _id, **kwargs):
        invoice = cls._get(_id)
        invoice.status = True
        invoice._id = int(_id)
        invoice.save()

    @classmethod
    def _get_sum(cls, spec, limit=10, offset=0):
        datas = cls._query(spec, limit=limit, offset=offset)
        for invoice in datas:
            invoice._invoice = InterFace.get_sum_invoice(invoice._invoice)
        return datas


class OfferInfo(Doc):

    structure = dict(
        _id=int,
        affiliate_id=int,
        offer_id=int,
        payout=float,
        actions=int,
        amount=float,
        click=int,
        currency=str,
        createdTime=str,
    )

    indexes = []

    @classmethod
    def sort_limit(cls, condition, count, *args, **kwds):
        result = []
        for i in  cls._collection.find(*args, **kwds).sort(condition).limit(count):
            i['_id'] = str(i['_id'])
            result.append(i)
        return map(lambda doc: cls(doc, collection=cls._collection), result)

    @classmethod
    def get_range_data(cls, affiliate_id=None, currency=None, start=None, end=None, offer_ids=None):
        spec = OrderedDict()
        if affiliate_id:
            spec.update(dict(affiliate_id={"$in": affiliate_id}))
        if currency:
            spec.update(dict(currency=currency))
        if start and end:
            spec.update(dict(createdTime={'$gte': start, '$lte': end}))
        if offer_ids:
            spec.update(dict(offer_id={'$in': offer_ids}))
        data = cls.find(spec)
        return data

    @classmethod
    def get_sum(cls, affiliate_id, currency, start, end):
        data = cls.get_range_data(affiliate_id, currency,  start, end)
        # data_sum {'1': {'offer': '', 'paryout': '', 'actions': '', ...}}
        data_sum = InterFace.get_sum(data)
        return [v for k, v in data_sum.items()]


if __name__ == '__main__':
    o = OfferInfo(dict(
        _id=_gid(GidKey.invoice_key),
        affiliate_id=71,
        offer_id=15,
        payout=500,
        actions=5,
        amount=40,
        click=100,
        currency='U.S.$',
        createdTime='2016-03-08',
    ))
    o.save()
    # i = Invoice.find()
    pass
