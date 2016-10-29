# coding=utf-8
from solo.web.mongo import Doc


class OfferList(Doc):
    structure = dict(
        _id=int,  # advertiser id
        offer_list=list,
    )


if __name__ == "__main__":
    # advs_id = [138, 61, 111, 86, 35, 91, 137, 42, 96]
    # for ad_id in advs_id:
    #     offer_list = OfferList(
    #         dict(
    #             _id=ad_id,
    #             offer_list=[]
    #         )
    #     )
    #     offer_list.save()
    pass
