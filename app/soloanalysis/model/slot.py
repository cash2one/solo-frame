# coding:utf-8
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid


class Slot(Doc):
    structure = dict(
        slot=list,
    )
