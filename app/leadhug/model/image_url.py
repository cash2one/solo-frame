# coding=utf-8
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid


class ImgUrl(Doc):
    structure = dict(
        _id=int,
        url=str,
        cname=str
    )
