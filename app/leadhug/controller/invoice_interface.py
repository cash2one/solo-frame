# coding=utf-8
from collections import defaultdict
import _env  # noqa
from app.leadhug.model.offers import Offers


class InterFace(object):

    @classmethod
    def get_sum(cls, data):
        data_dict = {}
        for doc in data:
            offer_id = doc.offer_id
            offer = Offers.find_one(dict(_id=int(offer_id)))
            # offer = Offers.find_one(dict(_id=int(offer_id)))
            data_dict.setdefault(offer_id, defaultdict(lambda: 0))
            data_dict[offer_id]['offer_id'] = offer_id
            data_dict[offer_id]['offer_name'] = offer.title
            data_dict[offer_id]['payout'] += doc.payout
            data_dict[offer_id]['actions'] += doc.actions
            data_dict[offer_id]['amount'] += doc.amount

        return data_dict

    @classmethod
    def get_sum_invoice(cls, data):
        data_dict = defaultdict(lambda: 0)
        for doc in data:
            # data_dict['payout'] += doc['payout']
            data_dict['actions'] += doc['actions']
            data_dict['amount'] += doc['amount']
            data_dict['real_pay'] += doc['real_pay']

        return data_dict