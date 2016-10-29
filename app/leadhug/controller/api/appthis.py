# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def get_report():
    """
    """
    http = httplib2.Http()
    url = "http://feed.appthis.com/feed/v1?api_key=2b749940922e74c65292a6da90e5dc01&format=json"
    headers = {
        "Content-Type": "application/json"
    }
    response, content = http.request(url, 'GET', headers=headers)
    offers = yajl.loads(content)['offers']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=86)).offer_list if OfferList.find_one(dict(_id=86)) else [] ##
    for k, v in offers.iteritems():
        for campaign in v['campaigns']:
            if not v['icon_url'].startswith('http'):
                v['icon_url'] = 'http:' + v['icon_url']
            if campaign['platform'] == 'Android':
                campaign['platform'] = '2'
            if campaign['platform'] == 'iPhone':
                campaign['platform'] = '1'
            o = dict(
                advertiser_id=86,
                is_api=True,
                offer_type=1,
                category_id=10,
                title=v['name'],
                platform=campaign['platform'],
                package_name=v['android_package_name'],
                click_url=v['tracking_url'] + "?clickid={clickid}&source={affid}&source2={aff_sub2}",#done
                icon_url=v['icon_url'],
                desciption=v['description'],
                total_cap=10000000,
                day_cap=10000000,
                month_cap=10000000,
                cap=dict(
                    day=10000000,
                    month=10000000,
                    total=10000000
                ),
                payment=float(campaign['payout'])*0.9,
                geo_targeting=campaign['countries'],
                conversions=0,
                revenue=float(campaign['payout']),
                status='1',
                access_status='1'
            )
            o = Offers(o)
            re = Offers.find_one(dict(title=o.title, geo_targeting=o.geo_targeting, platform=o.platform))
            if re:
                offers_list_new.append(re._id) ##
                re.is_expired = False ##
                re.advertiser_id = o.advertiser_id
                re.is_api = o.is_api
                re.offer_type = o.offer_type
                re.category_id = o.category_id
                re.title = o.title
                re.platform = o.platform
                re.package_name = o.package_name
                re.click_url = o.click_url
                re.icon_url = o.icon_url
                re.desciption = o.desciption
                re.total_cap = o.total_cap
                re.day_cap = o.day_cap
                re.month_cap = o.month_cap
                re.cap = o.cap
                re.payment = o.payment
                re.geo_targeting = o.geo_targeting
                re.conversions = o.conversions
                re.revenue = o.revenue
                re.status = o.status
                re.access_status = o.access_status
                re.save()
            else:
                o._id = _gid('ApiKey')
                o.is_expired = False ##
                offers_list_new.append(o._id) ##
                o.save()
    offers_list = OfferList.find_one(dict(_id=86)) ##
    if offers_list: ##
        offers_list._id = 86 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=86, ##
                offer_list=offers_list_new ##
            ) ##
        ) ##
        offers_list.save() ##
    is_expired_offers = list(set(offers_list_old) - set(offers_list_new)) ##
    for offer_id in is_expired_offers: ##
        offer = Offers.find_one(dict(_id=offer_id)) ##
        try:
            offer.is_expired = True ##
            offer.save()
        except AttributeError:
            continue

if __name__ == "__main__":
    get_report()
    print _gid('ApiKey')
