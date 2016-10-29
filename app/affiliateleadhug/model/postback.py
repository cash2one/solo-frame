# coding=utf-8
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.affiliateleadhug.model import GidKey


class PostBackNotFound(BaseException):
    pass


class PostBack(Doc):
    structure = dict(
        _id=int,
        affiliate_id=int,
        url=str,
        createdTime=str,
        last_update=str,
        deleted=bool
    )

    _t = DateTime()

    default_values = dict(
        createdTime=_t.current_time,
        last_update=_t.current_time,
        deleted=False
    )

    @classmethod
    def add(cls, affiliate_id, url):
        post_back = PostBack(dict(
            _id=_gid(GidKey.post_back_key),
            affiliate_id=int(affiliate_id),
            url=url
        ), True)
        post_back.save()
        return True

    @classmethod
    def update(cls, _id, url):
        post_back = PostBack.find_one(dict(_id=int(_id)))
        if not post_back:
            raise PostBackNotFound
        post_back.url = url
        post_back.last_update = cls._t.current_time
        post_back.save()
        return post_back

    @classmethod
    def delete(cls, _id):
        post_back = PostBack.find_one(dict(_id=int(_id)))
        post_back.deleted = True
        post_back.last_update = cls._t.current_time
        post_back.save()
        return True

    @classmethod
    def query(cls, affiliate_id):
        return PostBack.find(dict(affiliate_id=int(affiliate_id), deleted=False))
