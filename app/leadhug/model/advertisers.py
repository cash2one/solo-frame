# coding=utf-8
from solo.web.mongo import Doc
from datetime import datetime
from app.leadhug.controller.tools import Tool, DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey


class Advertisers(Doc):
    structure = dict(
        _id=int,
        user_id=int,
        country=str,
        account_manager=int,
        pm=int,
        offer_count=int,
        white_list=list,
        create_time=str,
        last_update=str,
        status=str,  # 0 delete, 1 active, 2 pause
    )

    t = DateTime()
    required_fields = []
    default_values = {
        'create_time': t.current_time,
        'last_update': t.current_time,
    }

    @classmethod
    def _save(cls, **kwargs):
        kwargs.update(dict(_id=_gid(GidKey.advertiser_key)))
        ads = Advertisers(kwargs, True)
        ads.save()
        return ads

    @classmethod
    def _update(cls, ad_id, **kwargs):
        ads = cls.find_one(dict(_id=int(ad_id)))
        ads._id = int(ad_id)
        ads.country = kwargs['country']
        ads.white_list = kwargs['white_list']
        ads.account_manager = kwargs['account_manager']
        ads.pm = kwargs.get('pm')
        ads.last_update = cls.t.current_time
        ads.status = kwargs['status']
        ads.save()
        return ads
