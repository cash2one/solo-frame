# coding=utf-8

import _env  # noqa
import urllib
import httplib2
import yajl
from app.leadhug.model.offers import Offers
from app.web.model.gid import gid as _gid
import cgi
from app.leadhug.model.offer_list import OfferList ##


def get_report():
    """
    """
    http = httplib2.Http()
    url = "https://api.hasoffers.com/Apiv3/json?NetworkId=adattract&Target=Affiliate_Offer&Method=findMyApprovedOffers&api_key=43bc7b535a0a37560334f2b0aea03783476887b9bd574a6ef5c4ca073e74462d"
    headers = {
        "Content-Type": "application/json"
    }
    response, content = http.request(url, 'GET', headers=headers)
    offers = yajl.loads(content)['response']['data']
    offers_list_new = [] ##
    offers_list_old = OfferList.find_one(dict(_id=138)).offer_list if OfferList.find_one(dict(_id=138)) else [] ##
    for k, v in offers.iteritems():
        click_url = "https://api.hasoffers.com/Apiv3/json?NetworkId=adattract&Target=Affiliate_Offer&Method=generateTrackingLink&api_key=43bc7b535a0a37560334f2b0aea03783476887b9bd574a6ef5c4ca073e74462d&offer_id=" + str(k)
        response, click_url = http.request(click_url, 'GET', headers=headers)
        try:
            click_url = yajl.loads(click_url)['response']['data']['click_url']
        except TypeError:
            continue

        country_url = "https://api.hasoffers.com/Apiv3/json?NetworkId=adattract&Target=Affiliate_Offer&Method=getTargetCountries&api_key=43bc7b535a0a37560334f2b0aea03783476887b9bd574a6ef5c4ca073e74462d&ids%5B%5D=" + str(k)
        response, country_url = http.request(country_url, 'GET', headers=headers)
        try:
            country = yajl.loads(country_url)['response']['data'][0]['countries'].keys()
        except AttributeError:
            continue
        platform_url = "https://api.hasoffers.com/Apiv3/json?NetworkId=adattract&Target=Affiliate_OfferTargeting&Method=getRuleTargetingForOffer&api_key=43bc7b535a0a37560334f2b0aea03783476887b9bd574a6ef5c4ca073e74462d&offer_id=" + str(k)
        response, platform_url = http.request(platform_url, 'GET', headers=headers)
        try:
            platform_url = yajl.loads(platform_url)['response']['data'][0]['rule']['name']
        except IndexError:
            platform_url = ''
        icon_url = "https://api.hasoffers.com/Apiv3/json?NetworkId=adattract&Target=Affiliate_OfferFile&Method=findAll&api_key=43bc7b535a0a37560334f2b0aea03783476887b9bd574a6ef5c4ca073e74462d&filters%5Boffer_id%5D=" + str(k)
        response, icon_banner = http.request(icon_url, 'GET', headers=headers)
        try:
            icon_url = yajl.loads(icon_banner)['response']['data']['data'].values()[0]['OfferFile']['thumbnail']
            banner_url = yajl.loads(icon_banner)['response']['data']['data'].values()[0]['OfferFile']['url']
        except (AttributeError, KeyError, TypeError) as e:
            icon_url = ''
            banner_url = ''
        if platform_url == 'Android':
            platform = '2'
        elif platform_url == 'iOS' or 'iPhone':
            platform = '1'
        else:
            continue
        o = dict(
            advertiser_id=138,
            is_api=True,
            offer_type=1,
            category_id=10,
            title=v['Offer']['name'],
            preview_url=v['Offer']['preview_url'],
            platform=platform,
            click_url=click_url + "&transaction_id={clickid}&aff_sub={aff_sub2}&affiliate_id={affid}&aff_sub2={aff_sub1}",#done
            desciption=cgi.escape(v['Offer']['description']),
            total_cap=10000000,
            day_cap=10000000,
            month_cap=10000000,
            cap=dict(
                day=10000000,
                month=10000000,
                total=10000000
            ),
            payment=float(v['Offer']['default_payout'])*0.9,
            geo_targeting=country,
            conversions=0,
            revenue=float(v['Offer']['default_payout']),
            status='1',
            access_status='1',
            icon_url=icon_url,
            banner_url=banner_url
        )
        o = Offers(o)
        re = Offers.find_one(dict(title=o.title, geo_targeting=o.geo_targeting, platform=o.platform)) ##
        if re:
            offers_list_new.append(re._id) ##
            re.is_expired = False ##
            re.advertiser_id = o.advertiser_id
            re.is_api = o.is_api
            re.offer_type = o.offer_type
            re.category_id = o.category_id
            re.title = o.title
            re.preview_url = o.preview_url
            re.platform = o.platform
            re.click_url = o.click_url
            re.icon_url = o.icon_url
            re.banner_url = o.banner_url
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
    offers_list = OfferList.find_one(dict(_id=138)) ##
    if offers_list: ##
        offers_list._id = 138 ##
        offers_list.offer_list = offers_list_new ##
        offers_list.save() ##
    else: ##
        offers_list = OfferList( ##
            dict( ##
                _id=138, ##
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
