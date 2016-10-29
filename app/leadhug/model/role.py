# coding=utf-8
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey


class Role(Doc):
    '''
    Fields: permission 权限组 {mail: {create: True, delete: False, update: True, query: True}, invoice: {}, ...}
    '''
    structure = dict(
        _id=int,
        name=str,
        permission=dict,
        createdTime=str,
        last_update=str,
        deleted=bool
    )

    _t = DateTime()

    indexes = [
        {'fields': ['_id']},
        {'fields': ['name', 'deleted']},
    ]

    default_values = {
        'createdTime': _t.current_time,
        'last_update': _t.current_time,
        'deleted': False
    }

    @classmethod
    def affiliate(cls):
        return cls.find_one(dict(name='Affiliate'))

    @classmethod
    def advertiser(cls):
        return cls.find_one(dict(name='Advertiser'))

    @classmethod
    def finance(cls):
        return cls.find_one(dict(name='Finance'))

    @classmethod
    def am(cls):
        return cls.find_one(dict(name='AM'))

    @classmethod
    def bd(cls):
        return cls.find_one(dict(name='BD'))

    @classmethod
    def pm(cls):
        return cls.find_one(dict(name='PM'))

    @classmethod
    def _create(cls, **kwargs):
        role = Role(gen_skel=True)
        role._id = _gid(GidKey.role_key)
        role.name = kwargs.get('name')
        role.permission = kwargs.get('permission')
        role.save()

    @classmethod
    def _delete(cls, _id):
        role = cls._get(_id)
        role.deleted = True
        role.save()

    @classmethod
    def _get(cls, _id):
        return cls.find_one(dict(_id=int(_id)))

    @classmethod
    def _update(cls, _id, **kwargs):
        role = cls._get(_id)
        role.name = kwargs.get('name', role.name)
        role.permission = kwargs.get('permission', role.permission)
        role.last_update = cls._t.current_time
        role.save()


if __name__ == '__main__':
    content = dict(name='affiliate', permission={})
    Role._create(**content)