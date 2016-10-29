# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
from app.leadhug.model.offer_list import OfferList ##


def parse_offer(offer):
    if offer['caps_daily'] == 'unlimited':
        offer['caps_daily'] = 10000000
    if offer['caps_total'] == 'unlimited':
        offer['caps_total'] = 10000000
    if ','.join(offer['targeting']['allowed']['os']) == 'Android':
        platform = '2'
    if ','.join(offer['targeting']['allowed']['os']) == 'iOS':
        platform = '1'
    o = dict(
            advertiser_id=91,
            is_api=True,
            offer_type=1,
            category_id=10,
            package_name=offer['app_id'],
            title=offer['name'],
            preview_url=offer['target_url'],
            desciption=offer['description'],
            day_cap=offer['caps_daily'],
            month_cap=10000000,
            total_cap=offer['caps_total'],
            cap=dict(
                day=offer['caps_daily'],
                month=10000000,
                total=offer['caps_total']
            ),
            click_url=offer['link'] + "&clickid={clickid}&clk_source_id={affid}", #done
            icon_url=offer['icon'],
            payment=float(offer['payout'])*0.9,
            platform=platform,
            geo_targeting=offer['targeting']['allowed']['countries'],
            rating=int(offer['rating']['votes']),
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
    url = "http://cpactions.com/api/v1.0/feed/public/offers?site_id=10459&hash=bfd486e491d72d38c533af53ee3c47b3097bafed&filters[avg_cr][gt]=0.01"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response, content = http.request(url, 'GET', headers=headers)
    offers = yajl.loads(content)['offers']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=91)).offer_list if OfferList.find_one(dict(_id=91)) else [] ##
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
            re.payment = o.payment
            re.platform = o.platform
            re.geo_targeting = o.geo_targeting
            re.rating = o.rating
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
    offers_list = OfferList.find_one(dict(_id=91)) ##
    if offers_list: ##
        offers_list._id = 91 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=91, ##
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