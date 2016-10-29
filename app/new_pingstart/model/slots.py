#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from enum import IntEnum
from datetime import datetime
from collections import OrderedDict
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid
from app.new_pingstart.model import GidKey


class SlotNotFound(BaseException):
    pass


class OperateNotAllowed(BaseException):
    pass


class STATUS(IntEnum):
    CLOSE = 0
    OPEN = 1


STATUS_HUMAN = {
    STATUS.CLOSE: "Closed",
    STATUS.OPEN: "Open"
}


class TYPE(IntEnum):
    SHUFFLE = 1
    NATIVE = 2
    INTERSTITIAL = 3
    BANNER = 4

TYPE_MAP = {
    '2': 'Native',
    '3': 'Interstitial',
    '4': 'Banner'
}


class PLATFORM(IntEnum):
    ANDROID = 1
    IOS = 2


class FILLING(IntEnum):
    FB = 1
    PS = 2


class Slots(Doc):
    '''
        :param  name 广告位名字
                category app类型
                appName app 名字
                keyword 关键词屏蔽
                appId 广告位所属useid
                request 请求次数
                click 点击次数
                platform 手机系统
                soltType 广告位类型
                version app版本
                model app other
                appBlackList app黑名单
    '''
    structure = dict(
        _id=int,
        name=str,
        status=STATUS,
        platform=PLATFORM,
        slotType=TYPE,
        category=str,
        appName=str,
        keyword=list,
        appId=int,
        version=str,
        network=[
            {
                'network_id': int,
                'network_name': str,
                'is_auth': bool,
                'is_paused': bool,
                'placement_id': dict,
                'adapter': str,
                'priority': int,
            }
        ],
        model={
            'app': bool,
            'other': bool
        },
        appBlackList=list,
        last_operated=str,
        first_filing=FILLING,
        deleted=bool
    )

    indexes = [
        {'fields': ['_id']},
        {'fields': ['appId', 'deleted']},
    ]
    default_values = {
        'deleted': False,
        'last_operated': lambda: datetime.now().strftime('%Y-%m-%d'),
        'model': {"app": True, "other": True},
        'appBlackList': [],
    }

    @property
    def status_human(self):
        return STATUS_HUMAN.get(self.status, 'Unknow')

    @classmethod
    def get_list(cls, user_id, keyword="", limit=20, offset=0):
        spec = OrderedDict(appId=user_id, deleted={"$ne": True})
        if keyword:
            spec.update({
                'name':  {
                    '$regex': keyword,
                }
            })
        return cls.find(spec, limit=limit, skip=offset, sort=[('_id', -1)]), Slots.count(spec)

    @classmethod
    def get_facebook_slots(cls, appId):
        condition = OrderedDict(appId=int(appId), facebook_id={
                                "$exists": True, "$ne": ""})
        return cls.find(condition,
                        {"appId": 1, "_id": 1, "facebook_id": 1, "name": 1})

    @classmethod
    def change_status(cls, slot_id, user_id, status):
        slot = cls.find_one(dict(_id=slot_id))
        if not slot:
            raise SlotNotFound()
        if not slot.appId == user_id:
            raise OperateNotAllowed()
        slot.status = status
        slot.last_operated = datetime.now().strftime('%Y-%m-%d')
        slot._id = int(slot._id)
        slot.save()
        return slot

    @classmethod
    def edit(cls, user_id, slot_id, slot_type, name, first_filing=None, keyword=None):
        data = {
            'slotType': slot_type,
            'name': name,
        }
        if slot_id:
            slot = cls.find_one(dict(_id=slot_id))
            slot._id = int(slot._id)
            if not slot:
                raise SlotNotFound()
            if not slot.appId == user_id:
                raise OperateNotAllowed()
            if slot_type == TYPE.SHUFFLE:
                raise OperateNotAllowed('can not create shuffle type slot')
            slot.last_operated = datetime.now().strftime('%Y-%m-%d')
            slot.update(data)
            slot.save()
        else:
            slot_id = int(_gid(GidKey.slot_key))
            data.update({
                '_id': slot_id,
                'appId': user_id,
                'status': STATUS.OPEN,
                'first_filing': FILLING.FB,
            })
            slot = Slots(data,True)
            slot.save()

        return slot


if __name__ == '__main__':
    # for slot in Slots.get_list(1004, offset=19):
    #     print(dict(slot))
    # pass
    docs = Slots.get_facebook_slots(1107)
    for i in docs:
        print i
