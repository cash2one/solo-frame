
# coding:utf-8
import codecs
import csv
import hashlib
import json
import os
from yajl import loads
import datetime
from _route import route
from app.leadhug.controller.tools import DateTime, Tool
from app.leadhug.controller.upload.file_upload_s3 import UploadS3
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.email import EMail
from app.leadhug.model.image_url import ImgUrl
from app.leadhug.view._base import JsonLoginView, View, LoginView
from app.leadhug.model.offers import Offers, PRICEMODEL
from app.leadhug.model.user import User
from app.leadhug.model.offer_affiliate import OfferAffiliate as OAffiliate
from app.web.model.gid import gid
from solo.lib.jsob import JsOb
from solo.lib.utils import is_email
from app.leadhug.model.category import Category
from app.leadhug.model.advertisers import Advertisers
from app.leadhug.model.country import Country as c
from app.leadhug.controller.scheduler.interface import ScheInterface


@route("/offer_affiliate")
class OfferAffiliate(LoginView):

    def get(self):
        status = {'0': 'Paused', '1': 'Active', '2': 'Pending'}
        offer_id = self.get_argument('offer_id')
        offer = Offers.find_one(dict(_id=int(offer_id)))
        if not offer:
            self.write(u'The offer is not exist!')
            return
        offer.status = status.get(offer.status)
        if offer.advertiser_id:
            ad = User._get(offer.advertiser_id)
            offer['advertiser'] = ad.account if ad else ''

        category = Category.find_one(_id=int(offer.category_id)) if offer.category_id else None
        offer['category'] = category.name if category else ''

        category = Category.find_one(_id=int(offer.category_id)) if offer.category_id else None
        offer['category'] = category.name if category else ''

        if offer.access_status == '1':
            offer.access_status = 'Public'
        elif offer.access_status == '2':
            offer.access_status = 'Need Approve'
        else:
            offer.access_status = 'Private'

        if offer.platform == '1':
            offer.platform = 'IOS'
        elif offer.platform == '2':
            offer.platform = 'ANDROID'
        elif offer.platform == '0':
            offer.platform = 'All'

        offer_affiliates = OAffiliate._query(offer_ids=[offer_id])
        for off_aff in offer_affiliates:
            affiliate = User.find_one(dict(_id=int(off_aff.affiliate_id)))
            affiliate_extend = Affiliate.find_one(dict(user_id=int(off_aff.affiliate_id)))
            if not affiliate_extend or not affiliate_extend.account_manager:
                off_aff['am_name'] = ''
            elif off_aff.status == '1':
                am = User.find_one(dict(_id=int(affiliate_extend.account_manager)))
                off_aff['am_name'] = am.account
            off_aff['affiliate_name'] = affiliate.account if affiliate else ''
            if off_aff.status == '1':
                off_aff['application_status'] = 'Approved'
            elif off_aff.status == '2':
                off_aff['application_status'] = 'Pending'
            else:
                off_aff['application_status'] = 'Rejected'

        self.render(
            offer=offer,
            offer_affiliates=offer_affiliates
        )


@route('/offers/create')
class CreateOffer(LoginView):

    def get(self):
        advertiser_extends = Advertisers.find(dict(status='1'))
        ads = User.find(dict(_id={'$in': [int(ad.user_id) for ad in advertiser_extends]}, deleted=False))
        cat = Category._query()
        self.render(
            ads=ads,
            cat=cat,
            countries=c().countries
        )

    def post(self):
        kw = Offers.get_parm(self)
        include_geos = kw.get('geo_targeting')
        exclude_geos = kw.get('exclude_geo_targeting')
        geos = c().countries
        if include_geos:
            for geo in include_geos:
                geos.pop(geo)
            kw['exclude_geo_targeting'] = geos.keys()
        elif not exclude_geos:
            kw['geo_targeting'] = geos.keys()
        offer = Offers._save(**kw)
        self.redirect("/offer_affiliate?offer_id={}".format(offer._id))


@route('/offers/delete/(\d+)')
class DeleteOffer(LoginView):

    def get(self, offer_id):
        err = JsOb()
        offer = Offers.find_one(dict(_id=int(offer_id)))
        if not offer:
            err.ad_info = "not found!"
        if err:
            self.render(err)
        else:
            offer.deleted = True
            offer._id = int(offer._id)
            offer.save()
        self.redirect("/offers/manage")


@route('/offers/modify/(\d+)')
class ModifyOffer(LoginView):

    def get(self, offer_id):
        advertiser_extends = Advertisers.find(dict(status={"$ne": '0'}))
        ads = User.find(dict(_id={'$in': [int(ad.user_id) for ad in advertiser_extends]}, deleted=False))
        cat = Category._query()
        offer = Offers.find_one(dict(_id=int(offer_id)))
        self.render(
            cat=cat,
            ads=ads,
            offer_id=offer_id,
            offer=offer,
            countries=c().countries
        )

    def post(self, offer_id):
        kw = Offers.get_parm(self, type='modify')
        include_geos = kw.get('geo_targeting')
        exclude_geos = kw.get('exclude_geo_targeting')
        geos = c().countries
        if include_geos:
            for geo in include_geos:
                geos.pop(geo)
            kw['exclude_geo_targeting'] = geos.keys()
        elif not exclude_geos:
            kw['geo_targeting'] = geos.keys()
        Offers._update(offer_id, **kw)
        self.redirect("/offers/manage")


@route('/offers/manage')
class ManageOffer(LoginView):
    def get(self):
        self.render()


@route("/j/offers_title")
class ManagerOffer(JsonLoginView):

    def get(self):
        id_or_name = self.get_argument('q')
        spec = dict()
        if id_or_name.isdigit():
            spec.update({
                '_id': int(id_or_name)
            })
        else:
            spec.update({
                'title':  {
                    '$regex': id_or_name,
                    '$options': "$i"
                }
            })
        offers = Offers.find(spec, {'title': 1}, limit=10)
        offers = [
            {'first_name': i._id, 'last_name': i.title} for i in offers
        ]
        self.finish(json.dumps(offers))


@route("/j/offers/manager")
class ManagerOffer(JsonLoginView):

    def post(self):
        _ids = self.json.offer_ids
        status = self.json.status
        is_api = self.json.is_api
        category = self.json.category
        price_model = self.json.price_model
        advertiser = self.json.advertiser
        country = self.json.country
        payment_min = self.json.payment_min
        payment_max = self.json.payment_max
        limit = 100 if not self.json.limit else int(self.json.limit)
        page = 1 if not self.json.page else int(self.json.page)
        skip = (page - 1) * limit
        is_api = True if is_api == '1' else {"$ne": True}
 
        query = {'is_api': is_api}
        if _ids:
            query["_id"] = {"$in": [int(id) for id in _ids]}
        if status:
            query["status"] = status
        if category:
            query["category"] = category
        if price_model:
            query["price_model"] = price_model
        if advertiser:
            query["advertiser"] = advertiser
        if country:
            country_list = country.split(',')
            query["geo_targeting"] = country if len(country_list) == 1 else {'$in': country_list}
        if payment_max or payment_min:
            query["payment"] = {}
        if payment_min:
            query["payment"]["$gte"] = float(payment_min)
        if payment_max:
            query["payment"]["$lte"] = float(payment_max)

        offers_count = Offers.count(query)
        offers = Offers.find(query, sort=[('_id', 1)], limit=limit, skip=skip)
        advertiser_extends = Advertisers.find(dict(status={"$ne": '0'}))
        advertisers = User.find(dict(_id={'$in': [int(ad.user_id) for ad in advertiser_extends]}, deleted=False))
        categories = Category.find(dict(status={"$ne": '0'}))
        for offer in offers:
            if offer.status == '0':
                offer.status = 'Paused'
            elif offer.status == '1':
                offer.status = 'Active'
            else:
                offer.status = 'Pending'

            if offer.price_model == '1':
                offer.price_model = 'CPA'
            elif offer.price_model == '2':
                offer.price_model = 'CPS'
            elif offer.price_model == '3':
                offer.price_model = 'CPC'

            if offer.advertiser_id:
                ad = User.find_one(dict(_id=int(offer.advertiser_id)))
                offer['advertiser'] = ad.account
            if offer.category_id:
                category = Category.find_one(dict(_id=int(offer.category_id)))
                offer['category'] = category.name
        self.finish(dict(
                offers_count=offers_count,
                offers=offers,
                advertisers=advertisers,
                categories=categories,
            )
        )


@route("/offers/banner_img")
class Upload(View):

    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__), 'upload/')
        resp = self.request.files['files[]'][0]
        body = resp['body']
        ext = os.path.splitext(resp['filename'])[1]
        cname = str(hashlib.md5(body).hexdigest()) + ext
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        url_obj = ImgUrl.find_one({'cname': cname})
        if not url_obj:
            fpath = upload_path + cname
            f = open(fpath, 'w')
            f.write(body)
            u = UploadS3(fpath, cname)
            res = u.upload_start()
            if res.done():
                url = 'https://leadhugstatic.s3.amazonaws.com/' + cname
                img = ImgUrl(dict(
                    _id=gid('leadhug_imgUrl'),
                    url=url,
                    cname=cname
                    )
                )
                img.save()
            else:
                url = "Upload failure!"
            os.remove(fpath)
        else:
            url = url_obj.url
        self.finish(dict(url=url))


@route("/report/export")
class OfferExport(LoginView):

    def get(self):
        filter = loads(self.get_argument('filter', ''))
        offer_id = filter.get('offer_id')
        is_api = filter.get('is_api')
        status = filter.get('status')
        category = filter.get('category')
        price_model = filter.get('price_model')
        advertiser = filter.get('advertiser')
        country = filter.get('geo', '')
        payment_min = filter.get('payout_min')
        payment_max = filter.get('payout_mix')

        is_api = True if is_api == '1' else {"$ne": True}
        query = {"is_api": is_api}
        if offer_id:
            query["_id"] = int(offer_id)
        if status:
            query["status"] = status
        if category:
            query["category"] = category
        if price_model:
            query["price_model"] = price_model
        if advertiser:
            query["advertiser"] = advertiser
        if country:
            country_list = country.split(',')
            query["geo_targeting"] = country if len(country_list) == 1 else {'$in': country_list}
        if payment_max or payment_min:
            query["payment"] = {}
        if payment_min:
            query["payment"]["$gte"] = float(payment_min)
        if payment_max:
            query["payment"]["$lte"] = float(payment_max)
        offers = Offers.find(query, sort=[('_id', 1)])
        fields = ['_id', 'name', 'category', 'payout_model', 'advertiser', 'payout', 'revenue', 'preview_url', 'geo_count', 'clicks', 'conversions', 'day_cap', 'total_cap']
        result_offers = []
        for offer in offers:
            if offer.status == '0':
                offer.status = 'Paused'
            elif offer.status == '1':
                offer.status = 'Active'
            else:
                offer.status = 'Pending'

            if offer.price_model == '1':
                offer.price_model = 'CPA'
            elif offer.price_model == '2':
                offer.price_model = 'CPS'
            elif offer.price_model == '3':
                offer.price_model = 'CPC'

            if offer.advertiser_id:
                ad = User.find_one(dict(_id=int(offer.advertiser_id)))
                offer['advertiser'] = ad.account
            if offer.category_id:
                category = Category.find_one(dict(_id=int(offer.category_id)))
                offer['category'] = category.name
            off_tmp = dict(
                _id=offer._id,
                name=offer.title,
                category=offer.get('category'),
                payout_model=offer.price_model,
                advertiser=offer.get('advertiser'),
                payout=offer.payment,
                revenue=offer.revenue,
                preview_url=offer.preview_url,
                geo_count=len(offer.geo_targeting),
                clicks=offer.clicks,
                conversions=offer.conversions,
                day_cap=offer.day_cap,
                total_cap=offer.total_cap
            )
            result_offers.append(off_tmp)

        with open('offer.csv', 'wb') as f:
            f.write(codecs.BOM_UTF8)
            fieldnames = fields
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(result_offers)

        file = open('offer.csv', 'r')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=offer.csv')
        self.write(file.read())


@route("/offer/pause/add")
class OfferPause(JsonLoginView):

    def post(self):
        err = JsOb()
        pause_date = self.json.pause_date
        if not pause_date:
            err.pause_date = u'pause_date cat\'t be empty!'
        elif Tool.str_datetime(pause_date, '%Y-%m-%d %H:%M:%S') <= datetime.datetime.now():
            err.pause_date = u'The pause time can\'t less than Now!'

        if not err:
            self.offer_id = self.json.offer_id
            job_type = 'date'
            store_executor_alias = 'offer'
            process_count = 5
            max_instances = 100
            scheduler = ScheInterface(job_type, store_executor_alias, process_count)
            res = scheduler.add_date_job(pause, [self.offer_id], pause_date, max_instances, self.job_listener)
            if res:
                scheduler.sche.start()
                self.send_email(pause_date, self.offer_id)
                offer = Offers.find_one(dict(_id=int(self.offer_id)))
                offer.pause_job_set = True
                offer.last_update = DateTime().current_time
                offer.save()
            else:
                err.pause_date = 'Add pause job failure!'

        self.render(err)

    def send_email(self, pause_date, offer_id):
        offer = Offers.find_one(dict(_id=int(offer_id)))
        offer_affiliate = OAffiliate.find(dict(offer_id=int(offer_id), status='1'), dict(affiliate_id=1))
        affiliate_uses = User.find(dict(_id={"$in": [int(off_aff.affiliate_id) for off_aff in offer_affiliate]}), dict(email=1))

        emails = map(lambda user: user.email, affiliate_uses)
        if not emails:
            return False
        recivers = reduce(lambda email_1, email_2: email_1.extend(email_2), emails, [])
        content = dict(
            user_id=self.current_user_id,
            model_id=0,
            receiver=recivers,
            message=u'The offer named {offer} will be paused on {pause_date}'.format(offer=offer.title, pause_date=pause_date),
            subject=u'Leadhug offer paused notification',
            sender=self.current_user.account
        )
        EMail._create(**content)
        return True

    def job_listener(self, event):
        err = u'The offer {} pause job failure!'.format(self.offer_id)
        recivers = self.current_user.email
        content = dict(
            user_id=self.current_user_id,
            model_id=0,
            receiver=recivers,
            message=err,
            subject=u'Leadhug offer paused failure notification',
            sender=self.current_user.account
        )
        EMail._create(**content)


def pause(offer_id):
    offer = Offers.find_one(dict(_id=int(offer_id)))
    if offer:
        offer.status = '0'
        offer.last_update = DateTime().current_time
        offer.save()


         
         




