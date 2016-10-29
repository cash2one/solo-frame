# coding:utf-8
import _env  # noqa
from _route import route
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.user import User
from app.leadhug.view._base import JsonErrView, JsonLoginView
from solo.lib.jsob import JsOb
from app.leadhug.model.invoice import Invoice, CURRENCY_TYPES
from app.leadhug.controller.tools import DateTime as _t
from app.leadhug.model.invoice import OfferInfo
from yajl import loads


@route("/j/invoice/new")
class InvoiceView(JsonLoginView):

    def get(self):
        affiliate_id = self.get_argument('affiliate_id')
        affiliate_id = [int(aff_id) for aff_id in affiliate_id.split(',') if aff_id]
        currency = self.get_argument('currency')
        start = self.get_argument('start')
        end = self.get_argument('end')
        offer_info = OfferInfo.get_sum(affiliate_id=affiliate_id, currency=currency, start=start, end=end)
        for d in offer_info:
            d.update(dict(real_pay='', remark=''))
        self.finish(
            dict(
                offer_info=offer_info,
                currencys=CURRENCY_TYPES
            )
        )

    def post(self):
        content = loads(self.request.body)
        content['user_id'] = self.current_user_id
        invoice = content.get('_invoices')
        for i in invoice:
            i['real_pay'] = float(i['real_pay'])
        Invoice._create(**content)
        self.finish()


@route("/j/invoices")
class Invoices(JsonLoginView):

    def get(self):
        status_type = {'0': False, '1': True}
        affiliate_id = int(self.get_argument('affiliate_id'))
        status = self.get_argument('status')
        limit = int(self.get_argument('limit'))
        page = int(self.get_argument('page'))
        skip = (page - 1) * limit
        spec = dict(
            affiliate_id={"$in": [affiliate_id]} if affiliate_id else {'$ne': ''},
            status=status_type[status] if status else {'$ne': ''},
            currency=self.get_argument('currency', {'$ne': ''}),
            createdTime={
                '$gte': self.get_argument('start', _t.get_day(6)),
                '$lte': self.get_argument('end', _t.today),
            }
        )
        invoices = Invoice._get_sum(spec,limit=limit,offset=skip)
        invoice_count = Invoice.count(spec)
        for i in invoices:
            affiliate = User.find_one(dict(_id=int(i.affiliate_id)))
            i['affiliate_name'] = affiliate.account
        self.finish(dict(invoices=invoices,invoice_count=invoice_count))


@route("/j/invoice/update")
class Update(JsonLoginView):

    def post(self):
        invoice_id = self.json._id
        Invoice._update(invoice_id)
        self.finish()

