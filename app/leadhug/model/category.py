# coding=utf-8
from solo.web.mongo import Doc
from app.leadhug.controller.tools import Tool, DateTime
from datetime import datetime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey


class Category(Doc):
    structure = dict(
        _id=int,
        name=str,
        status=int,  # 0 deleted; 1 active; 2 pending;
        create_time=str,
        last_update=str,
    )

    _t = DateTime()

    default_values = dict(
        create_time=_t.current_time,
        last_update=_t.current_time,
    )

    @classmethod
    def _query(cls):
        cat = cls.find(dict(status={"$ne": '0'}))
        return cat

    @classmethod
    def _save(cls, name, status):
        cat = Category(dict(
            _id=_gid(GidKey.category_key),
            name=name,
            status=status
        ), True)
        cat.save()

    @classmethod
    def _update(cls, cat_id, **kwargs):
        cat = cls.find_one(dict(_id=int(cat_id)))
        cat._id = int(cat_id)
        cat.name = kwargs['name']
        cat.status = kwargs['status']
        cat.last_update = cls._t.current_time
        cat.save()
