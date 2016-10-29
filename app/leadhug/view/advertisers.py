# coding:utf-8
from yajl import loads

from _route import route
from app.leadhug.model.role import Role
from app.leadhug.view._base import JsonLoginView, LoginView
from app.leadhug.model.advertisers import Advertisers

from solo.lib.jsob import JsOb
from app.leadhug.model.user import User
from app.leadhug.model.offers import Offers
from solo.lib.utils import is_email, is_valid_password


@route('/advertisers/create')
class CreateAdvertiser(LoginView):

    def get(self):
        spec = dict(
            role_id=Role.bd()._id,
            deleted=False
        )
        account_managers = User.find(spec)
        pms = User.find(dict(role_id=Role.pm()._id, deleted=False))
        self.render(
            account_managers=account_managers,
            pms=pms
        )


@route('/advertisers/new/')
class Advertiser(JsonLoginView):

    def post(self):
        err = JsOb()
        name = self.json.name
        if not name:
            err.name = u'Advertiser name can\'t be empty!'
        elif User.count(dict(account=name)):
            err.name = u'The name has been used!'
        emails = self.json.email
        if not emails:
            err.email = u'email can\'t be empty!'
        else:
            emails = emails.replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err.email = u'Email not valid, email=%s' % e
                elif User.count(dict(email=e, deleted=False)):
                    err.email = u"email %s already be used!" % e

        password = self.json.password
        if not is_valid_password(password):
            err.password = u'The password not Valid!'
        skype_id = self.json.skype_id
        country = self.json.country
        account_manager = self.json.account_manager
        if not account_manager:
            err.account_manager = u'BD must selected!'
        pm = self.json.pm
        if not pm:
            err.pm = u'PM must selected!'
        status = self.json.status
        white_list = self.json.white_list
        white_list = white_list.split(',') if white_list else None

        if not err:
            user = User._create(**dict(
                email=emails,
                password=password,
                account=name,
                role_id=Role.advertiser()._id,
                skype_id=skype_id
            ))

            kw = dict(
                    user_id=user._id,
                    country=country,
                    account_manager=int(account_manager) if account_manager else None,
                    pm=int(pm) if pm else None,
                    offer_count=0,
                    white_list=white_list,
                    status=status,
                )
            advertiser = Advertisers._save(**kw)
            self.finish(dict(advertiser_id=user._id, err=False))
        else:
            self.render(err)


@route('/advertisers/delete/(\d+)')
class DeleteAdvertiser(LoginView):

    def get(self, ad_id):
        err = JsOb()
        ad = Advertisers.find_one(dict(_id=int(ad_id)))
        if not ad:
            err.ad_info = "not found!"
        if err:
            self.render(err)
        else:
            ad.status = '0'
            ad._id = int(ad._id)
            ad.save()
        self.redirect("/advertisers/manage")


@route('/advertisers/modify/(\d+)')
class ModifyAdvertiser(LoginView):

    def get(self, ad_id):
        advertiser = Advertisers.find_one(dict(user_id=int(ad_id)))
        white_list = advertiser.white_list
        advertiser.white_list = ','.join(white_list) if white_list else ''
        user = User._get(advertiser.user_id)
        spec = dict(deleted=False, role_id=Role.bd()._id)
        bds = User.find(spec)
        pms = User.find(dict(role_id=Role.pm()._id), deleted=False)
        if user:
            advertiser['name'] = user.account
            advertiser['email'] = ','.join(user.email)
            advertiser['skype_id'] = user.skype_id
            advertiser['password'] = user.password

        self.render(
            account_managers=bds,
            pms=pms,
            advertiser=advertiser
        )


@route('/advertisers/update/(\d+)')
class Advertiser(JsonLoginView):

    def post(self, ad_id):
        err = JsOb()
        content = self.json
        ad = User.find_one(dict(_id=int(content.user_id)))
        if not content.name:
            err.name = u'Advertiser name can\'t be empty!'
        elif content.name != ad.account and User.count(dict(account=content.name)):
            err.name = u'The name has been used!'

        if not content.email:
            err.email = u'email can\'t be empty!'
        else:
            emails = content.email.replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err.email = u'Email not valid, email=%s' % e
                elif e not in ad.email and User.count(dict(email=e, deleted=False)):
                    err.email = u"email %s already be used!" % e

        if content.password != ad.password and not is_valid_password(content.password):
            err.password = u'The password not Valid!'

        if not content.account_manager:
            err.bd = u'BD must selected!'

        if not content.pm:
            err.pm = u'PM must selected!'

        if not err:
            user = User._update(content.user_id, **dict(
                email=emails,
                password=content.password,
                account=content.name,
                skype_id=content.skype_id,
                role_id=Role.advertiser()._id
            ))

            kw = dict(
                country=content.country,
                account_manager=int(content.account_manager) if content.account_manager else None,
                pm=int(content.pm) if content.pm else None,
                white_list=content.white_list.split(',') if content.white_list else None,
                status=content.status,
            )

            advertiser = Advertisers._update(ad_id, **kw)
            self.finish(dict(advertiser_id=user._id, err=False))
        else:
            self.render(err)


@route('/advertiser/detail/(\d+)')
class AdvertiserDetail(LoginView):

    def get(self, ad_id):
        ad = Advertisers.find_one(dict(user_id=int(ad_id)))
        ad_user = User.find_one(dict(_id=int(ad_id)))
        if ad_user:
            ad['_id'] = ad_user._id
            ad['name'] = ad_user.account
            ad['email'] = ';'.join(ad_user.email)
            ad['skype_id'] = ad_user.skype_id
            bd = User.find_one(dict(_id=ad.account_manager))
            ad['bd'] = bd.account if bd else ''
            pm = User.find_one(dict(_id=ad.pm))
            ad['pm'] = pm.account if pm else ''
            offers_count = Offers.count(dict(advertiser_id=ad_user._id))
            ad['offers_count'] = offers_count
            status_map = {'0': 'Deleted', '1': 'Active', '2': 'Paused'}
            ad['status'] = status_map.get(ad.status)
            ad['white_list'] = ','.join(ad.white_list) if ad.white_list else ''
            self.render(advertiser=ad)
        else:
            self.write('The advertiser not exist!')


@route('/advertisers/manage')
class ManageAdvertiser(LoginView):

    def get(self):
        self.render()

@route('/advertisers/manage/j')
class ManageAdvertiser(LoginView):

    def get(self):
        status = self.get_argument('status', '')
        limit = int(self.get_argument('limit', '100'))
        page = int(self.get_argument('page', '1'))
        skip = (page - 1 ) * limit

        ads = Advertisers.find(dict(status={"$ne": '0'} if not status or status == '0' else status),limit=limit,skip=skip)
        ads_count = Advertisers.count(dict(status={"$ne": '0'} if not status or status == '0' else status),limit=limit,skip=skip)
        for ad in ads:
            if ad.user_id:
                # offer_count = Offers.count(dict(advertiser=str(ad.user_id)))
                user = User._get(ad.user_id)
                bd = User._get(ad.account_manager)
                ad.account_manager = bd.account
                if ad.pm:
                    pm = User._get(ad.pm)
                    ad.pm = pm.account
                else:
                    ad.pm = ''
                ad['name'] = user.account
                ad['email'] = user.email
                ad['skype_id'] = user.skype_id
                ad._id = user._id
                ad.status = 'Active' if ad.status == '1' else 'Pending'
                # ad.offer_count = offer_count


        self.finish(dict(ads=ads,ads_count=ads_count))


