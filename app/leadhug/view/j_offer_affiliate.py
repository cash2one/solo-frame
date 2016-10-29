# coding=utf-8
import requests
import urllib
from yajl import loads
import _env  # noqa
from _route import route
from app.leadhug.model.offer_affiliate import OfferAffiliate as OAffiliates
from app.leadhug.model.offers import Offers
from app.leadhug.model.role import Role
from app.leadhug.model.user import User
from app.leadhug.view._base import JsonLoginView
from solo.lib.jsob import JsOb
from app.leadhug.model.affiliates import Affiliate


@route("/j/(affiliate|offers)")
class OfferOrAffiliate(JsonLoginView):

    def get(self, action):
        obj_list = []
        if action == 'affiliate':
            offer_id = self.get_argument('offer_id')
            off_affs = OAffiliates._query(offer_ids=[offer_id])
            obj_ids = [off_aff.affiliate_id for off_aff in off_affs]
            affilate_extends = Affiliate.find(dict(account_manager={"$ne": ''}, status={'$ne': '0'}))
            objs = User.find(dict(_id={"$in": [int(aff.user_id) for aff in affilate_extends if aff.account_manager]}, deleted=False))
            res = dict(affiliates=obj_list)

        elif action == 'offers':
            affiliate_id = self.get_argument('affiliate_id')
            off_affs = OAffiliates._query(affiliate_id=affiliate_id)
            obj_ids = [off_aff.offer_id for off_aff in off_affs]
            objs = Offers.find({'status': {'$ne': '0'}, 'is_api': {"$ne": True}})
            res = dict(offers=obj_list)

        for obj in objs:
            if int(obj._id) not in obj_ids:
                obj_list.append(obj)

        self.finish(res)


@route("/j/offer/update")
class OfferUpdate(JsonLoginView):

    def post(self):
        offer = self.json.obj
        Offers._update(offer.get('_id'), **offer)
        pass


@route("/j/offer_affiliate/delete")
class OfferAffiliateDelete(JsonLoginView):

    def post(self):
        off_aff_id = self.json.off_aff_id
        res = OAffiliates._delete(off_aff_id)

        result = u'Successful' if res else u'Delete failure, off_aff_id={}'.format(off_aff_id)

        self.finish(dict(res=result))


@route("/j/offer_affiliate/new")
class OfferAffiliate(JsonLoginView):

    def post(self):
        err = JsOb()
        content = loads(self.request.body)
        if content.get('affiliate_ids'):
            affiliate_ids = [int(_id) for _id in content.get('affiliate_ids')]
            affiliates = User.find(dict(_id={'$in': affiliate_ids}))
            for aff in affiliates:
                content['affiliate_id'] = aff._id
                if not content.get('payout'):
                    offer = Offers.find_one(dict(_id=int(content.get('offer_id'))))
                    content['payout'] = offer.payment
                OAffiliates._save(**content)

        elif content.get('offer_ids'):
            offer_ids = [int(_id) for _id in content.get('offer_ids')]
            offers = Offers.find(dict(_id={'$in': offer_ids}))
            for offer in offers:
                content['offer_id'] = offer._id
                OAffiliates._save(**content)

        off_affs = OAffiliates.find(dict(status={'$ne': '0'}))
        self.finish(dict(off_affs=off_affs))


@route("/j/offer_affiliate/update")
class OfferAffiliateUpdate(JsonLoginView):

    def post(self):
        err = JsOb()
        content = loads(self.request.body)
        off_aff_id = content.get('_id')
        res = OAffiliates._update(**content)
        if not res:
            err.error = u'update OfferAffiliate failure! ID={}'.format(off_aff_id)


@route("/j/offer_affiliate/post_back/click")
class PostBackTest(JsonLoginView):

    def post(self):
        click_url = self.json.click_url
        self.redirect_url_list = []
        if not click_url.startswith('http') and not click_url.startswith('https'):
            click_url = '{http}://{click_url}'.format(http='http', click_url=click_url)
        redirect_url_list = self.get_res(click_url)
        self.finish(dict(redirect_url_list=redirect_url_list))

    def get_res(self, click_url):
        res = requests.get(click_url, allow_redirects=False, verify=False)
        _store = res.headers._store
        if res.status_code in [302, 301]:
            if _store.get('location'):
                redirect_url = _store.get('location')[1]
            if not redirect_url.startswith('http') and not redirect_url.startswith('https'):
                click_url = click_url.split('main')[0]
                redirect_url = '{http}main/{redirect_url}'.format(http=click_url, redirect_url=redirect_url)
            self.redirect_url_list.append({'operate': res.status_code, 'url': redirect_url})
            return self.get_res(redirect_url)
        elif res.status_code == 200:
            if _store.get('refresh'):
                redirect_url = _store.get('refresh')[1].split('url=')[1]
                self.redirect_url_list.append({'operate': 'REFRESH', 'url': redirect_url})
                return self.get_res(redirect_url)
            else:
                self.redirect_url_list.append({'operate': res.status_code, 'url': ''})
            return self.redirect_url_list
        elif res.status_code == 404:
            self.redirect_url_list.append({'operate': res.status_code, 'url': click_url})
            return self.redirect_url_list
