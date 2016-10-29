# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def parse_offer(offer):
    if offer['platform'] == 'ANDROID':
        offer['platform'] = '2'
    else:
        offer['platform'] = '1'
    # if offer['gaid_must']:
    s = 'gaid={aff_sub1}'
    # else:
    #     s = 'gaid='
    o = dict(
            advertiser_id=137,
            is_api=True,
            offer_type=1,
            category_id=10,
            package_name=offer['pkgname'],
            title=offer['title'],
            desciption=offer['description'],
            day_cap=offer['remaining_daily_cap'],
            month_cap=10000000,
            total_cap=10000000,
            cap=dict(
                day=offer['remaining_daily_cap'],
                month=10000000,
                total=10000000
            ),
            click_url=offer['ad_url'].replace("gaid=", s) + "&sub_pub={aff_sub2}&pb=http%3a%2f%2fnative.solo-launcher.com%2fbulk%2finstall%3ffrom%3dLeadhugTest%26clickid%3d{clickid}",#done
            icon_url=offer['icon_url'],
            mini_version=offer['min_os_version'],
            payment=float(offer['payout'])*0.9,
            platform=offer['platform'],
            geo_targeting=offer['countries'],
            banner_url=offer['creatives'][0]['url'],
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
    url_ios = "http://api.acekoala.com/api/offers?app_key=4603af3476d9b60bfc5d5cdaa577bdca&platform=Ios"
    url_android = "http://api.acekoala.com/api/offers?app_key=4603af3476d9b60bfc5d5cdaa577bdca&platform=Android"
    # url_ios = "http://api.acekoala.com/api/offers?app_key=8dedbea4d48580075b14cd083e5c5f8e&platform=Android"
    # url_android = "http://api.acekoala.com/api/offers?app_key=8dedbea4d48580075b14cd083e5c5f8e&platform=Android&country=us,ru"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response_ios, content_ios = http.request(url_ios, 'GET', headers=headers)
    response_android,content_android = http.request(url_android, 'GET', headers=headers)
    offers_ios = yajl.loads(content_ios)['data']
    offers_android = yajl.loads(content_android)['data']
    offers = offers_ios + offers_android
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=137)).offer_list if OfferList.find_one(dict(_id=137)) else [] ##
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
    offers_list = OfferList.find_one(dict(_id=137)) ##
    if offers_list: ##
        offers_list._id = 137 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=137, ##
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
