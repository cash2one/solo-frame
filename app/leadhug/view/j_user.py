# coding:utf-8
import _env  # noqa
from _route import route
from app.leadhug.controller.tools import DateTime
from app.leadhug.model.role import Role
from app.leadhug.view._base import JsonErrView, JsonLoginView
from app.leadhug.model.user import User, UserNotFoundError,\
    PasswordNotMatchError
from app.web.model.captcha import captcha_new, captcha_verify
from solo.lib.jsob import JsOb
from solo.lib.utils import is_email, is_valid_password
from app.web.model.session import Session
from solo.config import HOST, SESSION_EXPIRE


@route('/j/login')
class UserLogin(JsonErrView):

    def _session_new(self, account, user_id):
        session = Session.new(user_id)
        self.set_cookie('S', session, domain="." + HOST,
                        expires_days=SESSION_EXPIRE)
        self.set_cookie('E', account, domain="auth." +
                        HOST, expires_days=SESSION_EXPIRE)

    def post(self):
        err = JsOb()
        if not self.json.email:
            err.email = 'Please input email'
        elif not is_email(self.json.email):
            err.email = 'Email not valid'
        if not self.json.password:
            err.password = 'Please input password'
        if not self.json.captcha_code:
            err.captcha_code = 'Please input captcha code'
        elif not captcha_verify(self.json.captcha_key, self.json.captcha_code):
            err.captcha_code = 'captcha code incorrect'

        if not err:
            try:
                user = User.verify(self.json.email, self.json.password)
                if user:
                    if user._role == 'Affiliate' or user._role == 'Advertiser':
                        err.email = u'You don\'t have a login permissions!'
                    else:
                        self._session_new(self.json.email, user._id)
                        user.last_login = DateTime().current_time
                        user.save()
            except UserNotFoundError:
                err.email = "email not found"
            except PasswordNotMatchError:
                err.password = "password incorrect"

        self.render(err)


@route('/j/user/new')
class Create(JsonLoginView):

    def post(self):
        err = JsOb()
        form = self.json

        if not form.email:
            err.email = 'Please input email'
        else:
            emails = form.email.replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err.email = 'Email not valid, email=%s' % e
                elif User.count(dict(email=e, deleted=False)):
                    err.email = "email %s already in use" % e

        if not form.account:
            err.account = 'Pleast input your account'

        if not form.password:
            err.password = 'Please input password'
        elif not is_valid_password(form.password):
            err.password = 'Password not valid'

        kw = dict(
            email=emails,
            password=form.password,
            account=form.account,
            role_id=form.role_id,
            skype_id=form.skype_id,
            phone=form.phone
        )

        if not err:
            user = User._create(**kw)

        self.render(err)


@route("/j/user/update")
class UserUpdate(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.json._id
        user_edit = User._get(user_id)
        if not self.json.account:
            err.account = u'Account not be empty!'
        elif self.json.account != user_edit.account and User.count(dict(account=self.json.account, deleted=False)):
            err.account = u'Account already in use!'

        if not self.json.email:
            err.email = u'Email not be empty!'
        else:
            emails = self.json.email.replace(' ', '').split(',')
            for e in emails:
                if not is_email(e):
                    err.email = 'Email not valid, email=%s' % e
                elif e not in user_edit.email and User.count(dict(email=e, deleted=False)):
                    err.email = "email %s already in use" % e

        if self.json.password:
            if self.json.password != user_edit.password and not is_valid_password(self.json.password):
                err.password = u'password not valid!'

        if not err:
            content = dict(
                account=self.json.account,
                role_id=self.json.role_id,
                email=emails,
                password=self.json.password,
                skype_id=self.json.skype_id,
                phone=self.json.phone
            )
            res = User._update(user_id, **content)
            if not res:
                err.update = u'update user:{} failure'.format(user_id)

        self.render(err)


@route('/j/user/delete')
class Delete(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.json.user_id

        if not user_id:
            err.user_error = u'user_id can\'t be empty!'
            self.render(err)
        if not err:
            user = User._delete(user_id)
            self.finish(dict(user=user))


@route('/j/user/manage')
class User_manage(JsonLoginView):

    def post(self):
        limit = int(self.json.limit)
        page = int(self.json.page)
        if self.current_user.is_admin:
            users = User.find({"deleted": False})
        else:
            users = [self.current_user]
        new_users = []
        for user in users:
            if user._role != 'Affiliate' and user._role != 'Advertiser':
                user['role'] = user._role
                new_users.append(user)

        users_count = len(new_users)
        start = (page - 1) * limit
        end = start + limit
        result = new_users[start:end]
        self.finish(dict(users=result, users_count=users_count))


@route('/j/captcha')
class _(JsonErrView):

    def get(self):
        captcha = {}
        key, token, b64img = captcha_new()
        captcha['key'] = key
        captcha['img'] = b64img
        self.finish(captcha)


@route("/j/roles")
class Roles(JsonLoginView):

    def get(self):
        roles = Role.find(dict(name={"$nin": ['Affiliate', 'Advertiser']}))
        self.finish(dict(roles=roles))


@route("/j/password/verify")
class VerifyPassword(JsonLoginView):

    def post(self):
        password = self.json.password
        _password = User.encrypt_pwd(self.json.password)
        if self.current_user.password != _password:
            res = u'Password Not Right!'
        else:
            res = u'Ok!'
        self.finish(dict(res=res))


@route("/j/new_password/verify")
class VerifyNewPassword(JsonLoginView):

    def post(self):
        res = User.password_verify(self.json.password)
        self.finish(dict(res=res))


@route("/j/password_confirm/verify")
class VerifyPassowrdConfirm(JsonLoginView):

    def post(self):
        if self.json.new_password != self.json.confirm_password:
            res = u'Two password is not consistent'
        else:
            res = u'Ok!'
        self.finish(dict(res=res))


@route("/j/password/modify")
class PasswordModify(JsonLoginView):

    def post(self):
        err = JsOb()
        form = self.json
        if not form.new_password:
            err.password = u'Please input password'
        elif not is_valid_password(form.new_password):
            err.password = u'Password not valid'
        new_password = User.encrypt_pwd(self.json.new_password)

        if not err:
            self.current_user.password = new_password
            self.current_user._id = int(self.current_user_id)
            self.current_user.save()

        self.render(err)


