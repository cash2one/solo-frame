# coding:utf-8

from _route import route
from _base import View, JsonLoginView, LoginView
from app.leadhug.model.offers import Offers
from app.leadhug.model.invoice import Invoice, OfferInfo
from app.leadhug.model.report_hour import ReportHour
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.user import User
from app.leadhug.model.offer_affiliate import OfferAffiliate


@route('/dashboard')
class DashBoard(LoginView):

    def get(self):
        user_id = self.current_user_id
        affiliate = Affiliate.find_one(dict(user_id=int(user_id)))
        user = User.find_one(dict(_id=int(affiliate.account_manager)))
        lastest_offers = Offers.sort_limit(
            [('_id', -1)], 10, dict(status={'$ne': '0'}, is_api={'$ne': True}))
        deloffers = []
        for offer in lastest_offers:
            off_aff = OfferAffiliate.find_one(
                dict(offer_id=int(offer._id), affiliate_id=user_id, deleted=False))
            if off_aff:
                if off_aff.payout:
                    offer.payment = off_aff.payout
                if offer.access_status == '0' and off_aff.status != '1':
                    deloffers.append(offer)
            else:
                if offer.access_status == '0':
                    deloffers.append(offer)
        for i in deloffers:
            lastest_offers.remove(i)
        offer_infos = OfferInfo.sort_limit(
            [('amount', -1)], 10, dict(affiliate_id=user_id))
        # feature offers
        condition = []
        for i in offer_infos:
            condition.append({'_id': i.offer_id})
        if condition:
            high_income_offers = Offers.find(
                {'$or': condition, 'status': {'$ne': '0'}, 'is_api': {'$ne': True}})
            deloffers = []
            for offer in high_income_offers:
                off_aff = OfferAffiliate.find_one(
                    dict(offer_id=int(offer._id), affiliate_id=user_id, deleted=False))
                if off_aff:
                    if off_aff.payout:
                        offer.payment = off_aff.payout
                    if offer.access_status == '0' and off_aff.status != '1':
                        deloffers.append(offer)
                else:
                    if offer.access_status == '0':
                        deloffers.append(offer)
            for i in deloffers:
                high_income_offers.remove(i)
        else:
            high_income_offers = []
        self.render(
            account_manager=user,
            lastest_offers=lastest_offers,
            high_income_offers=high_income_offers,
        )


@route('/highcharts/data')
class HighCharts(JsonLoginView):

    """
    result:
    {
        'clicks':{
            'x':[],
            'y':[]
        },
        'conversions':{
            'x':[],
            'y':[]
        }
    }
    """

    def get(self):
        time = self.get_argument('time', None, strip=True)
        user_id = self.current_user_id
        # user_name = User.find_one(dict(_id=user_id)).account

        report = ReportHour.get_highcharts_data(time, user_id)
        clicks_y = []
        conversions_y = []
        x = []
        for item in report['result']:
            x.append(item['_id'])
            clicks_y.append(item['clicks'])
            conversions_y.append((item['conversions']))
        result = {
            'clicks': {
                'x': x,
                'y': clicks_y
            },
            'conversions': {
                'x': x,
                'y': conversions_y
            }
        }
        self.finish(result)
