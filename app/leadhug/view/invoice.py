# coding=utf-8
from _base import LoginView
from _route import route
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.invoice import CURRENCY_TYPES
from app.leadhug.model.role import Role
from app.leadhug.model.user import User


@route('/invoices')
class InvoiceList(LoginView):

    def get(self):
        affiliates = Affiliate.find(dict(status={'$ne': '0'}))
        affiliate_user_ids = [a.user_id for a in affiliates if a]
        affiliates = User.find(dict(role_id=int(Role.affiliate()._id), _id={'$in': affiliate_user_ids}))
        self.render(affiliates=affiliates)


@route('/invoice')
class InvoiceNew(LoginView):

    def get(self):
        affiliates = Affiliate.find(dict(status={'$ne': '0'}))
        affiliate_user_ids = [a.user_id for a in affiliates if a]
        affiliates = User.find(dict(role_id=int(Role.affiliate()._id), _id={'$in': affiliate_user_ids}))
        self.render(affiliates=affiliates, currencys=CURRENCY_TYPES)


if __name__ == '__main__':
    pass
