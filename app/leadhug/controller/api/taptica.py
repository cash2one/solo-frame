# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def parse_offer(offer):
    if ''.join(offer['Platforms']) == 'Android':
        platform = '2'
    else:
        platform = '1'
    o = dict(
            advertiser_id=96,
            is_api=True,
            offer_type=1,
            category_id=10,
            package_name=offer['MarketAppId'],
            title=offer['Name'],
            preview_url=offer['PreviewLink'],
            desciption=offer['Description'],
            day_cap=10000000,
            month_cap=10000000,
            total_cap=10000000,
            cap=dict(
                day=10000000,
                month=10000000,
                total=10000000
            ),
            click_url=offer['TrackingLink'] + '&tt_aff_clickid={clickid}&tt_sub_aff={affid}&tt_advertising_id={aff_sub1}&pd={aff_sub2}',#done
            icon_url=offer['AppIconUrl'],
            mini_version=offer['MinOsVersion'],
            payment=float(offer['Payout'])*0.9,
            platform=platform,
            geo_targeting=offer['SupportedCountries'],
            banner_url=offer['Creatives'][0]['CreativeLink'],
            conversions=0,
            revenue=float(offer['Payout']),
            status='1',
            access_status='1'
     )
    return o


def get_report():
    """
    """
    http = httplib2.Http()
    url_ios = "https://api.taptica.com/v2/bulk?token=O%2fhjVq4UFGiM6fiHJBo2sw%3d%3d&platforms=iPhone"
    url_android = "https://api.taptica.com/v2/bulk?token=O%2fhjVq4UFGiM6fiHJBo2sw%3d%3d&platforms=android"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response_ios, content_ios = http.request(url_ios, 'GET', headers=headers)
    response_android,content_android = http.request(url_android, 'GET', headers=headers)
    offers_ios = yajl.loads(content_ios)['Data']
    offers_android = yajl.loads(content_android)['Data']
    offers = offers_ios + offers_android
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=96)).offer_list if OfferList.find_one(dict(_id=96)) else [] ##
    for offer in offers:
        o = Offers(parse_offer(offer))
        re = Offers.find_one(dict(title=o.title, geo_targeting=o.geo_targeting, click_url=o.click_url))
        if re:
            offers_list_new.append(re._id) ##
            re.is_expired = False ##
            re.advertiser_id = o.advertiser_id
            re.is_api = o.is_api
            re.offer_type = o.offer_type
            re.category_id = o.category_id
            re.package_name = o.package_name
            re.title = o.title
            re.preview_url = o.preview_url
            re.desciption = o.desciption
            re.day_cap = o.day_cap
            re.month_cap = o.month_cap
            re.total_cap = o.total_cap
            re.cap = o.cap
            re.click_url = o.click_url
            re.icon_url = o.icon_url
            re.mini_version = o.mini_version
            re.payment = o.payment
            re.platform = o.platform
            re.geo_targeting = o.geo_targeting
            re.banner_url = o.banner_url
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
    offers_list = OfferList.find_one(dict(_id=96)) ##
    if offers_list: ##
        offers_list._id = 96 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=96, ##
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
