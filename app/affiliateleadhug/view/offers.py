# coding:utf-8
from __future__ import division
import tornado
from _route import route
from _base import View, JsonLoginView, LoginView, JsonView
from app.leadhug.model.category import Category
from app.leadhug.model.invoice import OfferInfo
from app.leadhug.model.offers import Offers
from app.leadhug.model.offer_affiliate import OfferAffiliate
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.user import User
from solo.lib.jsob import JsOb
from app.leadhug.model.country import Country as _c
from tornado.escape import json_encode


@route("/offers")
class Offer(LoginView):

    def get(self):
        category = Category.find(dict(status={'$ne': '0'}))
        self.render(categories=category, countries=_c().countries)


@route('/offers/search')
class Search(LoginView):

    def get(self):
        spec = {"status": '1', "is_api": {"$ne": True}}
        fields = dict(
            _id=1, title=1, payment=1, access_status=1, preview_url=1)
        _type = self.get_argument('_type')
        country = self.get_arguments('countries[]')
        if country:
            spec.update(dict(geo_targeting=country))

        PriceModel = self.get_argument('price_model')
        if PriceModel:
            spec.update(dict(price_model=PriceModel))

        category = self.get_argument('categories')
        if category:
            spec.update(dict(category=category))

        min_payout = self.get_argument('payoutMin', 0)
        max_payout = self.get_argument('payoutMax', 10000)
        spec.update(
            dict(payment={'$gte': float(min_payout), '$lte': float(max_payout)}))

        limit = int(self.get_argument('limit', 20))
        page = int(self.get_argument('page', 1))

        id_or_name = self.get_argument('offerSearch')
        if id_or_name:
            if id_or_name.isdigit():
                spec.update(dict(_id=int(id_or_name)))
            else:
                spec.update(dict(title=id_or_name))

        if _type == 'need_approived':
            access_status = self.get_argument('access_status')
            if access_status:
                spec.update(dict(access_status=access_status))

            offers = Offers.find(spec, fields, sort=[('_id', -1)])
            offers = filter(self.filter_offer, offers)
        elif _type == 'applied':
            offers = Offers.find(spec, fields, sort=[('_id', -1)])
            offers = filter(self.filter_offer_apply, offers)
            application_status = self.get_argument('approvalStatus')
            if application_status:
                offers = filter(
                    lambda offer: offer['apply_status'] == application_status, offers)

        offers_count = len(offers)
        offers = offers[limit * (page - 1): limit * page]

        self.finish(
            dict(
                offers=offers,
                offers_count=offers_count
            )
        )

    def filter_offer(self, offer):
        off_aff = OfferAffiliate.find_one(
            dict(offer_id=int(offer._id), affiliate_id=self.current_user_id, deleted=False))
        if not off_aff or off_aff.status == '0':
            if offer.access_status != '0':
                return offer

    def filter_offer_apply(self, offer):
        url = "tracks.leadhug.com/lh/click?offer_id={0}&affiliate_id={1}&click_id={{clickid}}&aff_sub1={{aff_sub1}}"
        off_aff = OfferAffiliate.find_one(
            dict(offer_id=int(offer._id), affiliate_id=self.current_user_id, deleted=False))
        if off_aff:
            offer['apply_status'] = off_aff.status
            if off_aff.status == '1':
                offer['tracking_link'] = url.format(
                    offer._id, self.current_user_id)
            return offer


@route('/my_offers/search')
class Search(LoginView):

    def get(self):
        spec = {"status": '1'}
        is_api = self.get_argument('is_api')
        if is_api == '0':
            spec.update(dict(is_api={"$ne": True}))
        country = self.get_arguments('countries[]')
        if country:
            spec.update(dict(geo_targeting=country))

        PriceModel = self.get_argument('price_model')
        if PriceModel:
            spec.update(dict(price_model=PriceModel))

        category = self.get_argument('categories')
        if category:
            spec.update(dict(category=category))

        min_payout = self.get_argument('payoutMin', 0)
        max_payout = self.get_argument('payoutMax', 10000)
        spec.update(
            dict(payment={'$gte': float(min_payout), '$lte': float(max_payout)}))

        limit = int(self.get_argument('limit', 20))
        page = int(self.get_argument('page', 1))

        off_affs = OfferAffiliate.find(
            dict(affiliate_id=int(self.current_user_id), status='1', deleted=False))
        offer_ids = [int(off_aff.offer_id) for off_aff in off_affs]
        spec.update(dict(_id={'$in': offer_ids}))

        offers = Offers.find(spec, sort=[('_id', -1)])
        url = "tracks.leadhug.com/lh/click?offer_id={0}&affiliate_id={1}&click_id={{clickid}}&aff_sub1={{aff_sub1}}"
        for offer in offers:
            off_aff = OfferAffiliate.find_one(
                dict(offer_id=int(offer._id), affiliate_id=self.current_user_id, deleted=False))
            if off_aff.payout:
                offer.payment = off_aff.payout
            offer['tracking_link'] = url.format(
                offer._id, self.current_user_id)
            conversions = off_aff.get('conversions', 0) if off_aff.get(
                'conversions', 0) else 0
            clicks = off_aff.get('clicks', 0) if off_aff.get(
                'clicks', 0) else 0
            cost = off_aff.get('cost', 0) if off_aff.get('cost', 0) else 0

            offer['conversions'] = conversions
            offer['clicks'] = clicks
            offer['CR'] = float(
                conversions) / float(clicks) * 100 if clicks else 0
            offer['EPC'] = float(cost) / float(clicks) * 100 if clicks else 0
            offer['total'] = cost

        offers_count = len(offers)
        offers = offers[limit * (page - 1): limit * page]
        self.finish(
            dict(
                offers=offers,
                offers_count=offers_count
            )
        )


@route('/offers/detail')
class OfferDetail(LoginView):

    def get(self):
        offer_id = self.get_argument('offer_id', None, strip=True)
        offer = Offers.find_one(dict(_id=int(offer_id)))
        off_aff = OfferAffiliate.find_one(dict(
            offer_id=int(offer._id), affiliate_id=int(self.current_user_id), deleted=False))

        if offer.platform == '1':
            offer.platform = 'IOS'
        elif offer.platform == '2':
            offer.platform = 'ANDROID'
        elif offer.platform == '0':
            offer.platform = 'All'

        if off_aff:
            if off_aff.payout:
                offer.payment = off_aff.payout
            if off_aff.day_cap:
                offer.day_cap = off_aff.day_cap
            if off_aff.month_cap:
                offer.month_cap = off_aff.month_cap
            if off_aff.total_cap:
                offer.total_cap = off_aff.total_cap

            if offer.access_status == '1':
                offer['application_status'] = '1'
            if offer.access_status == '2':
                if off_aff.status == '1':
                    offer['application_status'] = '1'
                else:
                    offer['application_status'] = off_aff.status
        else:
            offer['application_status'] = '3'
        if offer.category_id:
            category = Category.find_one(dict(_id=int(offer.category_id)))
            if category:
                offer['category'] = category.name
        self.render(
            aff_id=self.current_user_id,
            offer=offer,
        )

    def post(self):
        pass


@route('/offers/apply')
class OfferApply(JsonLoginView):

    def post(self):
        err = JsOb()
        if not self.json._ids:
            err.apply = u'offer can\'t be Null!'

        if not err:
            offers = []
            for offer_id in self.json._ids:
                affiliate_id = self.current_user_id
                off_aff = OfferAffiliate.find_one(
                    dict(offer_id=int(offer_id), affiliate_id=int(affiliate_id), deleted=False))
                offer = Offers.find_one(dict(_id=int(offer_id)))
                status = '1' if offer.access_status == '1' else '2'
                if not off_aff:
                    off_aff = OfferAffiliate._save(
                        **dict(offer_id=int(offer_id), affiliate_id=int(affiliate_id), status=status, payout=offer.payment))
                else:
                    off_aff.payout = offer.payment
                    off_aff.status = status
                    off_aff.save()
                offers.append(offer)
            self.finish(dict(offers=offers, err=False))
        else:
            self.render(err)


@route('/offers/api')
class Search(JsonView):

    """
    默认每页 num:100
    page
    """

    def get(self):
        email = self.get_argument('email')
        pagenum = self.get_argument('pagenum', 100)
        page = self.get_argument('page', 1)
        status = self.get_argument(
            'status', 'all', strip=True)   # myOffers # all
        user = User.find_one(dict(email=email, deleted=False))
        if user:
            aff = Affiliate.find_one(
                dict(user_id=user._id, status={'$ne': '0'}))
            if aff:
                url = "http://tracks.leadhug.com/lh/click?offer_id={0}&affiliate_id={1}&click_id={{clickid}}&aff_sub1={{aff_sub1}}"
                if status == "all":
                    spec = {'is_api': True, 'is_expired': False}
                    offers = Offers.find(
                        spec, sort=[('_id', -1)], limit=int(pagenum), skip=(int(page)-1)*int(pagenum))
                    if page == 1:
                        to_api_offers = Offers.find(
                            dict(to_api=True, status='1'), sort=[('_id', -1)])
                    else:
                        to_api_offers = []
                    all_offers = offers+to_api_offers
                else:
                    spec = {"status": '1'}
                    off_affs = OfferAffiliate.find(
                        dict(affiliate_id=int(aff.user_id), status='1', deleted=False))
                    offer_ids = [int(off_aff.offer_id) for off_aff in off_affs]
                    spec.update(dict(_id={'$in': offer_ids}))
                    all_offers = Offers.find(spec, sort=[('_id', -1)])
                    for offer in all_offers:
                        off_aff = OfferAffiliate.find_one(
                            dict(offer_id=int(offer._id), affiliate_id=aff.user_id, deleted=False))
                        if off_aff.payout:
                            offer.payment = off_aff.payout
                for offer in all_offers:
                    offer['click_url'] = url.format(offer._id, aff.user_id)
                    offer['_id'] = int(offer['_id'])
                    if offer['platform'] == '1':
                        offer['platform'] = 'ios'
                    if offer['platform'] == '2':
                        offer['platform'] = 'android'
                    del offer['revenue']
                    del offer['clicks']
                    del offer['advertiser_id']
                    del offer['user']
                    del offer['conversions']
                    del offer['access_status']
                    del offer['last_update']
                    del offer['price_model']
                    del offer['status']
                    del offer['mini_version']
                    del offer['exclude_geo_targeting']
                    del offer['offer_type']
                    del offer['black_ip']
                    del offer['traffic_time']
                    del offer['create_time']
                    del offer['root']
                    del offer['is_api']
                    # del offer['offer_type']
                    del offer['category_id']
                    del offer['tag']
                    del offer['rating']
                    del offer['restrictions']
                    del offer['is_expired']
                    del offer['to_api']
                self.finish(json_encode(all_offers))

            else:
                self.finish('email invalid!')
        else:
            self.finish("email not found!")
