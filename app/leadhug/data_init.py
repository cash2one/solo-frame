# coding=utf-8
import sys
import os

path = os.path.join(os.getcwd(), "../../")
sys.path.append(path)
import _env  # noqa
from app.leadhug.controller.tools import DateTime
from app.leadhug.model import GidKey
from app.leadhug.model.role import Role
from app.leadhug.model.user import User
from app.web.model.gid import gid
from app.leadhug.model.offer_affiliate import OfferAffiliate
from app.leadhug.model.offers import Offers


def data_init():
    _t = DateTime()
    for r in ['AM', 'Affiliate', 'Advertiser', 'BD', 'PM']:
        role = Role(dict(
            _id=gid(GidKey.role_key),
            name=r,
            permission=[],
            createdTime=_t.current_time,
            last_update=_t.current_time,
            deleted=False
        ))
        role.save()

    user = User(dict(
        _id=gid(GidKey.user_key),
        account='admin',
        email=['admin@newborn-town.com'],
        password=User.encrypt_pwd(u'chizicheng521'),
        role_id='',
        is_admin=True,
        createdTime=_t.current_time,
        last_update=_t.current_time,
        last_login=_t.current_time,
        deleted=False
    ))
    user.save()


if __name__ == '__main__':
    data_init()

