# coding=utf-8
import hashlib
import re
from app.leadhug.model.role import Role
from solo.web.mongo import Doc
from app.leadhug.model import GidKey
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from solo.config import SECRET, DEBUG


class UserNotFoundError(BaseException):
    pass


class PasswordNotMatchError(BaseException):
    pass


class User(Doc):

    structure = dict(
        _id=int,
        account=str,
        email=list,
        password=str,
        skype_id=str,
        phone=str,
        role_id=int,
        parent_id=int,
        is_admin=bool,
        createdTime=str,
        last_update=str,
        last_login=str,
        deleted=bool
    )

    _t = DateTime()

    indexes = [
        {'fields': ['_id']},
        {'fields': ['account', 'deleted']},
    ]

    default_values = {
        'is_admin': False,
        'createdTime': _t.current_time,
        'last_update': _t.current_time,
        'last_login': _t.current_time,
        'deleted': False
    }

    @classmethod
    def _create(cls, **kw):
        password = kw.get('password', '')
        password = cls.encrypt_pwd(password)

        user = User(dict(
            _id=_gid(GidKey.user_key),
            email=kw.get('email'),
            password=password,
            account=kw.get('account'),
            role_id=int(kw.get('role_id')) if kw.get('role_id') else '',
            skype_id=kw.get('skype_id'),
            phone=kw.get('phone')
        ), True)
        user.save()
        return user

    @classmethod
    def _delete(cls, _id):
        user = cls._get(_id)
        user.deleted = True
        user.save()
        return user

    @classmethod
    def _update(cls, _id, **kw):
        user = cls._get(_id)
        role_id = kw.get('role_id')
        user.role_id = int(role_id) if role_id else user.role_id
        user.account = kw.get('account')
        user.email = kw.get('email')
        password = kw.get('password')
        user.password = cls.encrypt_pwd(password) if user.password != password else password
        user.skype_id = kw.get('skype_id')
        user.last_update = cls._t.current_time
        user.save()
        return user

    @classmethod
    def _update_account(cls, _id, **kw):
        password = kw.get('password', '')
        password = cls.encrypt_pwd(password)
        user = cls._get(_id)
        user.account = kw.get('account')
        user.email = kw.get('email')
        user.password = password
        user.skype_id = kw.get('skype_id')
        user.phone = kw.get('phone')
        user.last_update = cls._t.current_time
        user.save()
        return True

    @classmethod
    def _get(cls, _id):
        return cls.find_one(dict(_id=int(_id)))

    @classmethod
    def verify(cls, email, password):
        _password = cls.encrypt_pwd(password)

        user = cls.find_one(dict(email=email, deleted=False))

        if not user:
            raise UserNotFoundError()

        if _password != user.password:
            raise PasswordNotMatchError()

        return user

    @property
    def _role(self):
        if self.is_admin:
            return 'admin'
        role = Role.find_one(dict(_id=self.role_id))
        return role.name

    @classmethod
    def encrypt_pwd(cls, password):
        m = hashlib.md5(SECRET)
        m.update(password)
        password = m.hexdigest()
        return password

    @classmethod
    def _query(cls):
        spec = dict(deleted=False, is_admin=False)
        return cls.find(spec)

    @classmethod
    def password_verify(cls, password):
        pattern = re.compile('^([a-zA-Z]+)([0-9]+)[0-9A-Za-z]$')
        match = pattern.findall(password)
        if not match:
            res = u'password must be start with string and include number!'
        elif len(password) < 6:
            res = u'password must be greater than 6!'
        else:
            res = u'Ok!'
        return res


if __name__ == '__main__':
    content = {
        'account': 'admin@qq.com',
        'email': 'admin@qq.com',
        'password': '111',
        'role_id': 20
    }
    User._create(**content)
    # u = User.find_one(dict(_id=41))
    # u.password = User.encrypt_pwd('111')
    # u._id=41
    # u.save()