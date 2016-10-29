# coding:utf-8

from _route import route
from _base import LoginView, JsonLoginView
from app.leadhug.model.invoice import Invoice


@route('/payments')
class Payments(LoginView):

    def get(self):
        self.render()


@route('/j/payments')
class PaymentsPage(JsonLoginView):

    def post(self):
        affiliate_id = self.current_user_id
        limit = int(self.json.limit)
        page = int(self.json.page)
        invoices = Invoice._get_sum(spec=dict(
            affiliate_id=affiliate_id, status=True), limit=limit, offset=limit * (page - 1))
        invoices_count = Invoice.count(
            dict(affiliate_id=affiliate_id, status=True))
        self.finish(dict(invoices=invoices, invoices_count=invoices_count))
