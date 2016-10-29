#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from solo.config import HOST
from gid import gid
# from app.web.model._db import Doc
from solo.web.mongo import Doc


class Ob(Doc):
    structure = dict(
        id=int,
        name=str,
        ico=str,
        cid=int,
        crop=str,
    )

    indexes = [
        {'fields': ['id']},
        {'fields': ['cid']},
        {'fields': ['cid', 'name']},
    ]

    @classmethod
    def ob_get(cls, id):
        return Ob.find_one(dict(id=id))

    @staticmethod
    def new(name, cid=0):
        id = gid()
        o = Ob(dict(id=id, name=str(name), ico='', cid=int(cid)))
        o.save()
        return o

    def ico_new(self, ico, crop=None):
        self.ico = ico
        if crop is not None:
            self.crop = crop
        self.save()

    def rename(self, name):
        self.name = name
        self.save()

    @property
    def url(self):
        return "//%s.%s" % (self.id, HOST)

    @staticmethod
    def by_id_list(li):
        if li:
            return Ob.find({"id": {"$in": map(int, li)}})
        return []

    @property
    def ico_url(self):
        # FIXME
        return self.ico_url

    CAN_ADMIN = {}

    def can_admin(self, admin_id):
        return self.CAN_ADMIN[self.cid](int(admin_id), self.id)

    @staticmethod
    def cid_by_id(id):
        o = Ob.find_one({'id': id})
        if o:
            return o.cid


def ob_name_ico_by_id(id):
    ob = Ob.find_one({'id': id})
    return ob.name, ob.ico or 0


def ob_name_by_id(id):
    return Ob.find_one({'id': id}).name


def name_ico_dict_by_id_list(li):
    result = {}
    for i in Ob.by_id_list(li):
        result[i.id] = (str(i.name), i.ico or 0)
    return result


def name_dict_by_id_list(li):
    result = {}
    for i in Ob.by_id_list(li):
        result[i.id] = str(i.name)
    return result

if __name__ == '__main__':
    o = Ob(dict(id=11111, name=str('super mush'), ico=''))
    o.save()
    pass
