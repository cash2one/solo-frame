# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def parse_android_offer(offer):
    o = dict(
            advertiser_id=111,
            is_api=True,
            offer_type=1,
            category_id=10,
            package_name=offer['androidPackage'],
            title=offer['title'],
            preview_url="https://play.google.com/store/apps/details?id="+offer['androidPackage'],
            desciption=offer['desc'],
            day_cap=10000000,
            month_cap=10000000,
            total_cap=10000000,
            cap=dict(
                day=10000000,
                month=10000000,
                total=10000000
            ),
            click_url=offer['urlApp'] + '&id={clickid}&subid={aff_sub2}&did={aff_sub1}',#done
            icon_url=offer['urlImg'],
            mini_version=offer['supportedVersion'],
            payment=float(offer['revenueRate'])*0.9,
            platform='2',
            geo_targeting=offer['country'],
            conversions=0,
            revenue=float(offer['revenueRate']),
            status='1',
            access_status='1'
     )
    return o


def parse_ios_offer(offer):
    o = dict(
            advertiser_id=111,
            is_api=True,
            offer_type=1,
            category_id=10,
            package_name=offer['iphonePackage'] if offer.get('iphonePackage') else '',
            title=offer['title'],
            # preview_url=offer['PreviewLink'],
            desciption=offer['desc'],
            day_cap=10000000,
            month_cap=10000000,
            total_cap=10000000,
            cap=dict(
                day=10000000,
                month=10000000,
                total=10000000
            ),
            click_url=offer['urlApp'] + '&id={clickid}&subid={aff_sub2}&did={aff_sub1}',#
            icon_url=offer['urlImg'],
            mini_version=offer['supportedVersion'],
            payment=float(offer['revenueRate'])*0.9,
            platform='1',
            geo_targeting=offer['country'],
            conversions=0,
            revenue=float(offer['revenueRate']),
            status='1',
            access_status='1'
     )
    return o


def get_report():
    """
    """
    http = httplib2.Http()
    url_ios = "https://admin.appnext.com/offerApi.aspx?id=dbc2d386-5f74-4817-a0a6-1b688877ea24"
    url_android = "https://admin.appnext.com/offerApi.aspx?id=cdd8008b-da30-42e3-be36-c64c6bf536ea"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response_ios, content_ios = http.request(url_ios, 'GET', headers=headers)
    response_android,content_android = http.request(url_android, 'GET', headers=headers)
    offers_ios = yajl.loads(content_ios)['apps']
    offers_android = yajl.loads(content_android)['apps']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=111)).offer_list if OfferList.find_one(dict(_id=111)) else [] ##
    for offer in offers_ios:
        o = Offers(parse_ios_offer(offer))
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
            # re.preview_url = o.preview_url
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

    for offer in offers_android:
        o = Offers(parse_android_offer(offer))
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
    offers_list = OfferList.find_one(dict(_id=111)) ##
    if offers_list: ##
        offers_list._id = 111 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=111, ##
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
