# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import pprint
import yajl

from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def parse_offer(offer):
    if offer['platform'] == 'Android':
        offer['platform'] = '2'
    if offer['platform'] == 'iOS':
        offer['platform'] = '1'
    o = dict(
            advertiser_id=163,
            is_api=True,
            offer_type=1,
            category_id=10,
            title=offer['title'],
            platform=offer['platform'],
            package_name=offer['packageName'],
            mini_version=offer['minOSVersion'],
            click_url=offer['clickURL'] + "&p1=clickid&v1={clickid}&aff_sub1={aff_sub2}&deviceId={aff_sub1}",
            icon_url=offer['creatives'][0]['url'],
            total_cap=10000000,
            day_cap=10000000,
            month_cap=10000000,
            cap=dict(
                day=10000000,
                month=10000000,
                total=10000000
            ),
            desciption=offer['description'],
            payment=float(offer['bid'])*0.9,
            geo_targeting=offer['geoTargeting'],
            conversions=0,
            revenue=float(offer['bid']),
            status='1',
            access_status='1'
     )
    return o


def get_report():
    """
    """
    http = httplib2.Http()
    url = "http://api.apprevolve.com/v2/getAds?siteid=52486&token=piMUU11EfUa3NVd9RsEXEg"
    headers = {
        "Content-Type": "application/json"
    }
    response, content = http.request(url, 'GET', headers=headers)
    offers = yajl.loads(content)['ads']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=163)).offer_list if OfferList.find_one(dict(_id=163)) else [] ##
    for offer in offers:
        o = Offers(parse_offer(offer))
        re = Offers.find_one(dict(title=o.title, geo_targeting=o.geo_targeting, click_url=o.click_url))
        if re:
            offers_list_new.append(re._id) ##
            re.advertiser_id = re.advertiser_id
            re.is_api = o.is_api
            re.offer_type = o.offer_type
            re.category_id = o.category_id
            re.title = o.title
            re.platform = o.platform
            re.package_name = o.package_name
            re.mini_version = o.mini_version
            re.click_url = o.click_url
            re.icon_url = o.icon_url
            re.total_cap = o.total_cap
            re.day_cap = o.day_cap
            re.month_cap = o.month_cap
            re.cap = o.cap
            re.payment = o.payment
            re.geo_targeting = o.geo_targeting
            re.conversions = o.conversions
            re.desciption = o.desciption
            re.revenue = o.revenue
            re.status = o.status
            re.access_status = o.access_status
            re.is_expired = False ##
            re.save()
        else:
            o._id = _gid('ApiKey')
            o.is_expired = False ##
            offers_list_new.append(o._id) ##
            o.save()
    offers_list = OfferList.find_one(dict(_id=163)) ##
    if offers_list: ##
        offers_list._id = 163 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=163, ##
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
