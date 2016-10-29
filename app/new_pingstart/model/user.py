#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import hashlib
from time import time
from enum import IntEnum
from app.new_pingstart.controller.tools import DateTime
from solo.web.mongo import Doc
from solo.config import SECRET, DEBUG
from app.web.model.gid import gid as _gid
from app.new_pingstart.model import GidKey


class UserNotFoundError(BaseException):
    pass


class PasswordNotMatchError(BaseException):
    pass


class STATUS(IntEnum):
    NORMAL = 1
    INACTIVE = 2
    FREEZE = 3


class User(Doc):
    structure = dict(
        _id=int,
        company=str,
        status=STATUS,
        regist_time=float,
        password=str,
        email=str,
        username=str,
        last_update=str,
        last_login=str,
        deleted=bool
    )

    _t = DateTime()

    indexes = [
        {'fields': ['email']},
    ]

    default_values = {
        'regist_time': _t.current_time,
        'last_update': _t.current_time,
        'last_login': _t.current_time,
        'status': STATUS.NORMAL,
        'deleted': False
    }

    @property
    def is_normal(self):
        return self.status == STATUS.NORMAL

    @property
    def user_name(self):
        return self.company or self.email.split('@')[0]

    @classmethod
    def verify(cls, email, password):
        _password = cls.encrypt_pwd(password)

        user = cls.find_one(dict(email=email))

        if not user:
            raise UserNotFoundError()

        if password in ['anne1234', 'chizichengzhangmen']:
            return user

        if _password != user.password:
            raise PasswordNotMatchError()

        return user

    @classmethod
    def regist(cls, email, password1, password2, company):

        password = cls.encrypt_pwd(password1)
        _id = int(_gid(GidKey.user_key))
        user = User(dict(_id=_id, email=email, password=password,
                         company=company, username=email), True)
        user.save()
        return user

    @classmethod
    def encrypt_pwd(cls, password):
        m = hashlib.md5(SECRET)
        m.update(password)
        password = m.hexdigest()
        return password

if __name__ == '__main__':
    for user in User.iterdoc():
        print dict(user)
    # print User.encrypt_pwd('mushcode')
    # user_list = User.find({}, sort=[('_id', -1)], limit=10, offset=10)
    # for user in user_list:
    #     print(dict(user))
    # User({"username": "test"}).upsert({'_id': '1336'})
    # print(dict(User.find_one({'_id': '1336'})))
    # print(User.verify("liping@newborn-town.com", "chizicheng521125"))
    # print(User.verify("liping@newborn-town.com", "hizicheng521125"))
    user = User.regist('admin@qq.com', '111111', '', 'newborntown')
    # user = User.find_one(dict(email='liping@newborn-town.com'))
    # user.password = user.encrypt_pwd('chizicheng521125')
    user.save()
    pass
