# coding=utf-8
from enum import Enum
from solo.web.mongo import Doc
from app.leadhug.controller.tools import Tool, DateTime
from datetime import datetime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey
from bson.objectid import ObjectId


PRICEMODEL = {
    '3': 'CPC',
    '1': 'CPA',
    '2': 'CPS'
}

CATEGORIES = {

}


class Offers(Doc):
    structure = dict(
        _id=int,
        is_api=bool,
        title=str,
        category_id=int,
        price_model=str,  # 1 cpa, 2 cps, 3 cpc
        advertiser_id=int,
        tag=str,
        rating=int,
        platform=str,  # 0 all, 1 ios, 2 Android
        icon_url=str,
        package_name=str,
        mini_version=str,
        desciption=str,
        restrictions=str,
        click_url=str,
        clicks=int,
        conversions=int,
        preview_url=str,
        banner_url=str,
        conver_image=str,
        total_cap=int,
        day_cap=int,
        month_cap=int,
        cap={
            'day': int,
            'month': int,
            'total': int
        },
        payment=float,
        revenue=float,
        root=bool,
        geo_targeting=list,
        exclude_geo_targeting=list,
        offer_type=int,  # 1 Desktop, 2 Mobile, 3 Rejected
        create_time=str,
        last_update=str,
        traffic_time=str,
        access_status=str,  # 0 private, 1 Public, 2 Need Approve
        status=str,     # 0 paused, 1 active, 2 pending
        black_ip=list,
        user=str,
        is_expired=bool,  # 过期:true  没过期:false
        to_api=bool,     # 转成api：true  # 保持手动 ： false
        pause_job_set=bool  # True: has set; False: no set
    )

    default_values = {
        'traffic_time': '',
        'is_api': False,
    }

    @classmethod
    def sort_limit(cls, condition, count, *args, **kwds):
        result = []
        for i in  cls._collection.find(*args, **kwds).sort(condition).limit(count):
            i['_id'] = str(i['_id'])
            result.append(i)
        return map(lambda doc: cls(doc, collection=cls._collection), result)

    @classmethod
    def _save(cls, **kwargs):
        offer = Offers(kwargs, True)
        offer.save()
        return offer

    @classmethod
    def get_parm(cls, self, type=None):
        user = self.get_current_user().account
        title = self.get_argument('title', None, strip=True)
        category_id = self.get_argument('category', None, strip=True)
        price_model = self.get_argument('price_model', None,strip=True)
        advertiser_id = self.get_argument('advertiser', None, strip=True)
        tag = self.get_argument('tag', None, strip=True)
        rating = self.get_argument('rating', None, strip=True)
        platform = self.get_argument('platform', None, strip=True)
        icon_url = self.get_argument('icon_url', None, strip=True)
        package_name = self.get_argument('package_name', None, strip=True)
        mini_version = self.get_argument('mini_version', None, strip=True)
        desciption = self.get_argument('desciption', None, strip=True)
        restrictions = self.get_argument('restrictions', None, strip=True)
        click_url = self.get_argument('click_url', None, strip=True)
        banner_url = self.get_argument('banner_url', None, strip=True)
        preview_url = self.get_argument('preview_url', None, strip=True)
        conver_image = self.get_argument('conver_image', None, strip=True)
        total_cap = self.get_argument('total_cap', 0, strip=True)
        if not total_cap:
            total_cap = 0
        daily_cap = self.get_argument('daily_cap', 0, strip=True)
        if not daily_cap:
            daily_cap = 0
        month_cap = self.get_argument('month_cap', 0, strip=True)
        if not month_cap:
            month_cap = 0
        revenue = self.get_argument('revenue', None, strip=True)
        payment = self.get_argument('payment', None, strip=True)
        root = self.get_argument('root', None, strip=True)
        include_geo_targeting = self.get_arguments('include_geo_targeting')
        exclude_geo_targeting = self.get_arguments('exclude_geo_targeting')
        offer_type = self.get_argument('offer_type', 1, strip=True)
        status = self.get_argument('status', None, strip=True)
        access_status = self.get_argument('access_status', None, strip=True)
        black_ip = []
        to_api = True if self.get_argument('to_api', None, strip=True) == "true" else False
        now = datetime.now()
        create_time = Tool.datetime_str(now, "%Y%m%d-%H:%M:%S")
        last_update = Tool.datetime_str(now, "%Y%m%d-%H:%M:%S")

        kw = dict(
                title=title,
                category_id=int(category_id) if category_id else None,
                price_model=price_model,
                advertiser_id=int(advertiser_id) if advertiser_id else None,
                tag=tag,
                rating=rating,
                platform=platform,
                icon_url=icon_url,
                package_name=package_name,
                mini_version=mini_version,
                desciption=desciption,
                restrictions=restrictions,
                click_url=click_url,
                banner_url=banner_url,
                preview_url=preview_url,
                conver_image=conver_image,
                total_cap=int(total_cap) if total_cap else 10000000,
                day_cap=int(daily_cap) if daily_cap else 10000000,
                month_cap=int(month_cap) if month_cap else 10000000,
                cap=dict(
                    day=int(daily_cap) if daily_cap else 10000000,
                    month=int(month_cap) if month_cap else 10000000,
                    total=int(total_cap) if total_cap else 10000000
                ),
                revenue=float(revenue) if revenue else 0,
                payment=float(payment) if payment else 0,
                root=root,
                geo_targeting=include_geo_targeting,
                exclude_geo_targeting=exclude_geo_targeting,
                status=status,
                access_status=access_status,
                black_ip=black_ip,
                user=user,
                offer_type=offer_type,
                to_api=to_api,
                create_time=create_time,
                last_update=last_update,
                pause_job_set=False
            )
        if not type:
            kw['_id'] = _gid(GidKey.offer_key)
        return kw

    @classmethod
    def _update(cls, offer_id, **kwargs):
        now = datetime.now()
        last_update = Tool.datetime_str(now, "%Y%m%d-%H:%M:%S")
        offer = cls.find_one(dict(_id=int(offer_id)))
        offer._id = int(offer_id)
        offer.title = kwargs['title']
        offer.category_id = int(kwargs['category_id']) if kwargs.get('category_id') else None
        offer.advertiser_id = kwargs['advertiser_id']
        offer.price_model = kwargs['price_model']
        offer.tag = kwargs['tag']
        offer.rating = kwargs['rating']
        offer.platform = kwargs['platform']
        offer.icon_url = kwargs['icon_url']
        offer.package_name = kwargs['package_name']
        offer.mini_version = kwargs['mini_version']
        offer.desciption = kwargs['desciption']
        offer.restrictions = kwargs['restrictions']
        offer.click_url = kwargs['click_url']
        offer.banner_url = kwargs['banner_url']
        offer.preview_url = kwargs['preview_url']
        offer.conver_image = kwargs['conver_image']
        offer.total_cap = int(kwargs['total_cap']) if kwargs.get('total_cap') else 10000000
        offer.day_cap = int(kwargs['day_cap']) if kwargs.get('day_cap') else 10000000
        offer.month_cap = int(kwargs['month_cap']) if kwargs.get('month_cap') else 10000000
        offer.cap = dict(day=offer.day_cap, month=offer.month_cap, total=offer.total_cap)
        offer.revenue = float(kwargs['revenue']) if kwargs.get('revenue') else 0
        offer.payment = float(kwargs['payment']) if kwargs.get('payment') else 0
        offer.root = kwargs['root']
        offer.geo_targeting = kwargs['geo_targeting']
        offer.exclude_geo_targeting = kwargs['exclude_geo_targeting']
        offer.status = kwargs['status']
        offer.access_status = kwargs['access_status']
        offer.offer_type = kwargs['offer_type']
        offer.last_update = last_update
        offer.black_ip = kwargs.get('black_ip')
        offer.to_api = kwargs.get('to_api')
        offer.save()

    @classmethod
    def query(cls, start, end=None):
        if not end:
            end = DateTime().today

        spec = {
            'is_api': {"$ne": True},
            'traffic_time': {
                '$lte': end,
                '$gte': start
            }
        }
        return cls.find(spec)


if __name__ == '__main__':
    # spec = {'is_api': True, 'is_expired': {'$ne': True}}
    # offers = Offers.find(spec, sort=[('_id', -1)], skip=600, limit=100)
    # print len(offers)
    data = {
        "access_status" : "2",
        "advertiser_id" : 78,
        "banner_url" : "",
        "black_ip" : [ ],
        "cap" : {
                "total" : 10000000,
                "day" : 10000000,
                "month" : 10000000
        },
        "category_id" : None,
        "click_url" : "",
        "clicks" : None,
        "conver_image" : "",
        "conversions" : None,
        "create_time" : "20160531-19:49:38",
        "day_cap" : 10000000,
        "desciption" : "",
        "exclude_geo_targeting" : [ ],
        "geo_targeting" : [ ],
        "icon_url" : "",
        "is_api" : False,
        "is_expired" : None,
        "last_update" : "2016-06-02 00:00:00",
        "mini_version" : "",
        "month_cap" : 10000000,
        "offer_type" : 1,
        "package_name" : "",
        "pause_job_set" : True,
        "payment" : 0,
        "platform" : "0",
        "preview_url" : "",
        "price_model" : "1",
        "rating" : "",
        "restrictions" : "",
        "revenue" : 0,
        "root" : "No",
        "status" : "1",
        "tag" : "",
        "title" : "offer1",
        "to_api" : False,
        "total_cap" : 10000000,
        "traffic_time" : "",
        "user" : "admin"
    }

    for i in range(2000, 10000):
        data['_id'] = i
        Offers(data, True).save()

    pass
