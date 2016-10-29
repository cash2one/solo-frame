# coding=utf-8
from app.leadhug.controller.tools import DateTime
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey


class OfferAffiliate(Doc):
    structure = dict(
        _id=int,
        offer_id=int,
        affiliate_id=int,
        payout=float,
        day_cap=int,
        month_cap=int,
        total_cap=int,
        cost=float,
        cap=dict,
        status=str,  # 0 rejected, 1 approved, 2 pending
        create_time=str,
        last_update=str,
        traffic_time=str,
        clicks=int,
        conversions=int,
        deleted=bool  # 0 delete
    )

    _t = DateTime()

    default_values = {
        'create_time': _t.current_time,
        'last_update': _t.current_time,
        'traffic_time': '',
        'deleted': False
    }

    @classmethod
    def _save(cls, **kw):
        day_cap = 10000000
        month_cap = 10000000
        total_cap = 10000000
        if kw.get('day_cap'):
            day_cap = int(kw.get('day_cap'))
        if kw.get('month_cap'):
            month_cap = int(kw.get('month_cap'))
        if kw.get('total_cap'):
            total_cap = int(kw.get('total_cap'))
        offer_affiliate = OfferAffiliate(dict(
            _id=_gid(GidKey.off_aff_key),
            offer_id=int(kw.get('offer_id')),
            affiliate_id=int(kw.get('affiliate_id')),
            payout=float(kw.get('payout', 0)) if kw.get('payout') else 0,
            day_cap=day_cap,
            month_cap=month_cap,
            total_cap=total_cap,
            cap=dict(day=day_cap, month=month_cap, total=total_cap),
            status=kw.get('status', '2')
        ), True)

        offer_affiliate.save()
        return offer_affiliate

    @classmethod
    def _query(cls, offer_ids=None, affiliate_id=None):
        spec = {'deleted': False}
        if offer_ids:
            spec.update(dict(offer_id={"$in": [int(offer_id) for offer_id in offer_ids]}))

        if affiliate_id:
            spec.update(dict(affiliate_id=int(affiliate_id)))
        return cls.find(spec)

    @classmethod
    def _delete(cls, _id):
        if _id:
            off_aff = OfferAffiliate.find_one(dict(_id=int(_id)))
            off_aff.deleted = True
            off_aff.save()
            return True
        return False

    @classmethod
    def _update(cls, _id, **kw):
        off_aff = cls.find_one(dict(_id=int(_id)))
        if kw.get('affiliate_id'): off_aff.affiliate_id = int(kw.get('affiliate_id'))
        if kw.get('offer_id'): off_aff.offer_id = int(kw.get('offer_id'))
        if kw.get('payout'): off_aff.payout = float(kw.get('payout'))
        if kw.get('day_cap'): off_aff.day_cap = float(kw.get('day_cap'))
        if kw.get('month_cap'): off_aff.month_cap = float(kw.get('month_cap'))
        if kw.get('total_cap'): off_aff.total_cap = float(kw.get('total_cap'))
        off_aff.cap = dict(day=off_aff.day_cap, month=off_aff.month_cap, total=off_aff.total_cap),
        if kw.get('status'): off_aff.status = kw.get('status')
        off_aff.last_update = cls._t.current_time
        off_aff.save()
        return True

if __name__ == '__main__':
    OfferAffiliate.find({'offer_id': int(1)})