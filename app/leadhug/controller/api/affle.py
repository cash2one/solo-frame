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
    if offer['assetType'] == 'android':
        offer['assetType'] = '2'
    if offer['assetType'] == 'ios':
        offer['assetType'] = '1'
    o = dict(
            advertiser_id=61,
            is_api=True,
            offer_type=1,
            category_id=10,
            title=offer['campaignName'],
            platform=offer['assetType'],
            # package_name=offer['assetUrl'].split('=')[1],
            # mini_version=','.join(offer['targeting']['systemTargeting']['osVersion']),
            click_url=offer['defaultTrackerURL'].replace('{af_subid}','{affid}').replace('{af_advertising_id}','{aff_sub1}'),#done
            banner_url=offer['creatives'][0]['creativeURL'],
            preview_url=offer['assetUrl'],
            total_cap=10000000,
            day_cap=offer['dailyInstallCap'],
            month_cap=10000000,
            cap=dict(
                day=offer['dailyInstallCap'],
                month=10000000,
                total=10000000
            ),
            payment=float(offer['payout'])*0.9,
            geo_targeting=offer['targeting']['geoTargeting']['country'],
            create_time=offer['startDate'],
            conversions=0,
            revenue=float(offer['payout']),
            status='1',
            access_status='1'
     )
    return o


def get_report():
    """
    """
    http = httplib2.Http()
    url = "http://mapi.affle.co/publisher.php?cId=all&key=63389e65c6fe8cd5f7b2f8d12e698907"
    headers = {
        "Content-Type": "application/json"
    }
    response, content = http.request(url, 'GET', headers=headers)
    offers = yajl.loads(content)['data']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=61)).offer_list if OfferList.find_one(dict(_id=61)) else [] ##
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
            # re.package_name = o.package_name
            # re.mini_version = o.mini_version
            re.click_url = o.click_url
            re.banner_url = o.banner_url
            re.preview_url = o.preview_url
            re.total_cap = o.total_cap
            re.day_cap = o.day_cap
            re.month_cap = o.month_cap
            re.cap = o.cap
            re.payment = o.payment
            re.geo_targeting = o.geo_targeting
            re.create_time = o.create_time
            re.conversions = o.conversions
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
    offers_list = OfferList.find_one(dict(_id=61)) ##
    if offers_list: ##
        offers_list._id = 61 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=61, ##
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
