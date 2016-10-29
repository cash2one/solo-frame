# coding:utf-8
import json
import requests
from yajl import loads
from _route import route
from app.leadhug.model.offers import Offers
from app.leadhug.model.role import Role
from app.leadhug.model.user import User
from app.leadhug.view._base import JsonLoginView, LoginView
from app.leadhug.model.affiliates import Affiliate, InvoiceFrequency
from app.leadhug.model.offer_affiliate import OfferAffiliate as OAffiliate
from app.web.model.session import Session

from solo.lib.jsob import JsOb
from solo.lib.utils import is_email, is_valid_password


@route("/affiliate_offer")
class AffiliateOffer(LoginView):

    def get(self):
        affiliate_user_id = self.get_argument('affiliate_id')
        affiliate = Affiliate.find_one(dict(user_id=int(affiliate_user_id)))
        affiliate_user = User.find_one(dict(_id=int(affiliate_user_id)))
        if not affiliate or not affiliate_user:
            self.write(u'The affiliate is not exist!')
            return
        affiliate._id = affiliate.user_id
        affiliate['name'] = affiliate_user.account
        affiliate['email'] = affiliate_user.email
        affiliate['skype_id'] = affiliate_user.skype_id

        offer_affiliates = OAffiliate._query(affiliate_id=affiliate._id)
        for off_aff in offer_affiliates:
            offer = Offers.find_one(dict(_id=int(off_aff.offer_id)))
            off_aff['offer_title'] = offer.title if offer else ''
            if off_aff.status == '1':
                off_aff['application_status'] = 'Approved'
            elif off_aff.status == '2':
                off_aff['application_status'] = 'Pending'
            else:
                off_aff['application_status'] = 'Rejected'
        self.render(
            affiliate=affiliate,
            offer_affiliates=offer_affiliates
        )


@route('/affiliate/create')
class CreateAffiliate(LoginView):

    def get(self):

        spec = dict(
            role_id=Role.am()._id,
            deleted=False
        )
        account_managers = User.find(spec)
        self.render(account_managers=account_managers, invoice_frequency=InvoiceFrequency)

    def post(self):
        form = loads(self.request.body)
        err = {}
        if not form.get('email'):
            err['email'] = 'Please input email'
        else:
            emails = form['email'].replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err['email'] = 'Email not valid, email=%s' % e
                elif User.count(dict(email=e, deleted=False)):
                    err['email'] = "email %s already be used!" % e

        if not form.get('account'):
            err['account'] = 'Pleast input your account'
        elif User.count(dict(account=form.get('account'), deleted=False)):
            err['account'] = 'Account already be used!'

        if not form.get('password'):
            err['password'] = 'Please input password'
        elif not is_valid_password(form.get('password')):
            err['password'] = 'Password not valid'

        if not form.get('account_manager'):
            err['account_manager'] = 'Please select Account Manager!'

        if not err:
            kw = dict(
                email=emails,
                password=form.get('password'),
                account=form.get('account'),
                role_id=Role.affiliate()._id,
                skype_id=form.get('skype_id'),
                phone=form.get('phone')
            )
            user = User._create(**kw)
            form['user_id'] = user._id
            aff = Affiliate._save(**form)

        self.finish(dict(err=err if err else False))


@route('/affiliates/delete/(\d+)')
class DeleteAffiliate(LoginView):

    def get(self, aff_id):
        err = JsOb()
        aff = Affiliate.find_one(dict(_id=int(aff_id)))
        if not aff:
            err.ad_info = "not found!"
        if err:
            self.render(err)
        else:
            aff.deleted = True
            aff._id = int(aff._id)
            aff.save()
        self.redirect("/affilicates/manage")


@route('/affiliates/modify/(\d+)')
class ModifyAffiliate(LoginView):

    def get(self, aff_id):
        affiliate = Affiliate.find_one(dict(user_id=int(aff_id)))
        user = User._get(affiliate.user_id)
        spec = dict(deleted=False, role_id=Role.am()._id)
        account_managers = User.find(spec)
        affiliate['account'] = user.account
        affiliate['email'] = user.email
        affiliate['skype_id'] = user.skype_id
        affiliate['phone'] = user.phone
        affiliate['password'] = user.password

        self.render(
            account_managers=account_managers,
            affiliate=affiliate,
            invoice_frequency=InvoiceFrequency
        )

    def post(self, aff_id):
        affiliate_edit = Affiliate.find_one(dict(_id=int(aff_id)))
        user_edit = User._get(affiliate_edit.user_id)
        form = loads(self.request.body)
        err = {}
        if not form.get('email'):
            err['email'] = 'Please input email'
        else:
            emails = form['email'].replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err['email'] = 'Email not valid, email=%s' % e
                elif e not in user_edit.email and User.count(dict(email=e, deleted=False)):
                    err['email'] = "email %s already be used!" % e

        if not form.get('account'):
            err['account'] = 'Pleast input your account'
        elif form.get('account') != user_edit.account and User.count(dict(account=form.get('account'), deleted=False)):
            err['account'] = 'Account already be used!'

        if not form.get('password'):
            err['password'] = 'Please input password'
        elif form.get('password') != user_edit.password and not is_valid_password(form.get('password')):
            err['password'] = 'Password not valid'

        if not form.get('account_manager') and form.get('status') != '0':
            err['account_manager'] = 'Please select Account Manager!'

        if not err:
            kw = dict(
                email=emails,
                password=form.get('password'),
                account=form.get('account'),
                role_id=Role.affiliate()._id,
                skype_id=form.get('skype_id'),
                phone=form.get('phone'),
            )
            user = User._update(user_edit._id, **kw)
            aff = Affiliate._update(aff_id, **form)

        self.finish(dict(err=err if err else False))


@route('/affiliates/manage')
class ManageAffiliate(LoginView):

    def get(self):
            self.render(affs={})

    def post(self):
        status = self.get_argument('status', '')
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '100'))
        skip = (page - 1) * limit

        affs = Affiliate.find(dict(
            status={"$ne": '0'} if not status or status == '0' else status,
            # account_manager=int(self.current_user_id) if not self.current_user.is_admin else {'$ne': ''}
        ),limit=limit,skip=skip)
        for aff in affs:
            aff.status = 'Active' if aff.status == '1' else 'Pending'
            user = User._get(aff.user_id)
            if aff.account_manager:
                account_manager = User._get(aff.account_manager)
                aff.account_manager = account_manager.account
            aff['name'] = user.account
            aff['email'] = user.email
            aff['password'] = user.password
            aff['_id'] = user._id
            aff['skype_id'] = user.skype_id
            aff['phone'] = user.phone
            aff['offer_count'] = OAffiliate.count(dict(affiliate_id=int(aff._id)))
        affs_count = Affiliate.count(dict(
            status={"$ne": '0'} if not status or status == '0' else status,
            # account_manager=int(self.current_user_id) if not self.current_user.is_admin else {'$ne': ''}
        ))
  
        self.finish(dict(affs=affs,affs_count=affs_count))
    