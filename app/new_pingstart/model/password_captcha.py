# !/usr/bin/env python
# coding:utf-8
import _env  # noqa
from app.new_pingstart.controller.tools import DateTime
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid
from app.new_pingstart.model import GidKey


class Captcha(Doc):
    structure = dict(
        _id=int,
        email=str,
        code=str,
        create_time=str,
    )

    _t = DateTime()

    default_values = dict(
        create_time=_t.current_time
    )

    @classmethod
    def create(cls, email=None, captcha_code=None):
        captcha = Captcha.find_one(dict(email=email))
        if not captcha:
            captcha = Captcha(dict(
                _id=int(_gid(GidKey.captcha_key)),
                email=email,
                code=captcha_code
            ), True)
        else:
            captcha.code = captcha_code
            captcha.create_time = cls._t.current_time
        captcha.save()
        return captcha
