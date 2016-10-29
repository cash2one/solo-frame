# coding:utf-8
import random
from yajl import loads
import datetime
import _env  # noqa
from _route import route
from app.new_pingstart.controller.send_email import send_email
from app.new_pingstart.controller.tools import DateTime, Tool
from app.new_pingstart.model.password_captcha import Captcha
from app.new_pingstart.view._base import JsonErrView, JsonLoginView, View
from app.new_pingstart.model.user import User, UserNotFoundError,\
    PasswordNotMatchError
from app.new_pingstart.model.network import NetWork
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
                    self._session_new(user.email, user._id)
                    # user.last_login = DateTime().current_time
                    # user.save()
            except UserNotFoundError:
                err.email = "email not found"
            except PasswordNotMatchError:
                err.password = "password incorrect"

        self.render(err)


@route('/j/signup')
class SignUp(JsonErrView):

    def _session_new(self, account, user_id):
        session = Session.new(user_id)
        self.set_cookie('S', session, domain="." + HOST,
                        expires_days=SESSION_EXPIRE)
        self.set_cookie('E', account, domain="auth." +
                        HOST, expires_days=SESSION_EXPIRE)

    def post(self):
        err = JsOb()
        form = self.json

        if not form.email:
            err.email = 'Please input email'
        elif not is_email(form.email):
            err.email = 'Email not valid'
        elif User.count(dict(email=form.email)):
            err.email = "email already in use"

        if not form.password:
            err.password = 'Please input password'
        elif not is_valid_password(form.password):
            err.password = 'Password not valid'
        elif form.password != form.password2:
            err.password2 = 'Password not match'

        if not form.captcha_code:
            err.captcha_code = 'Please input captcha code'
        elif not captcha_verify(form.captcha_key, form.captcha_code):
            err.captcha_code = 'captcha code incorrect'

        if not err:
            user = User.regist(form.email, form.password,
                               form.password2, form.company)
            NetWork._init(user._id)
            self._session_new(user.email, user._id)

        self.render(err)


@route("/j/email_verify")
class ForgetPassword(View):

    def post(self):
        err = dict(signup=True)
        email = loads(self.request.body).get('email', '')
        user = User.find_one(dict(email=email, deleted=False))
        if not user:
            err['signup'] = False
        self.finish(err)


@route("/old_password_verify")
class ModifyPassword(JsonLoginView):

    def post(self):
        err = JsOb()
        user = self.current_user
        old_password = self.json.old_password
        if not old_password:
            err.old_password = 'Please input password!'
        elif not is_valid_password(old_password):
            err.old_password = 'Password not valid!'
        elif user.encrypt_pwd(old_password) != self.current_user.password:
            err.old_password = 'The password is incorrect!'

        self.render(err)


@route("/verify_password")
class VerifyPassword(JsonErrView):

    def post(self):
        err = JsOb()
        new_password = self.json.new_password
        if not new_password:
            err.new_password = 'Please input password!'
        elif not is_valid_password(new_password):
            err.new_password = 'Password not valid!'

        self.render(err)


@route("/verify_confirm")
class VerifyConfirm(JsonErrView):

    def post(self):
        err = JsOb()
        new_password = self.json.new_password
        confirm_password = self.json.confirm_password
        if not new_password:
            err.new_password = 'Please input password1'
        elif not is_valid_password(new_password):
            err.new_password = 'Password not valid!'

        if not confirm_password:
            err.confirm_password = 'Please input password!'
        elif not is_valid_password(confirm_password):
            err.confirm_password = 'Password not valid!'

        if new_password != confirm_password:
            err.confirm_password = 'The two passwords do not match!'

        self.render(err)


@route("/modify_password")
class ModifyPassword(JsonLoginView):

    def post(self):
        user = self.current_user
        password = self.json.password
        user.password = user.encrypt_pwd(password)
        user.last_update = DateTime().current_time
        user.save()


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
            emails = self.json.email.replace(' ', '').split(';')
            for e in emails:
                if not is_email(e):
                    err.email = 'Email not valid, email=%s' % e
                elif self.json.email not in user_edit.email and User.count(dict(email=e, deleted=False)):
                    err.email = "email %s already in use" % e

        if self.json.password:
            if self.json.password != user_edit.password and not is_valid_password(self.json.password):
                err.password = u'password not valid!'

        if not err:
            content = dict(
                account=self.json.account,
                email=self.json.email,
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


@route('/j/captcha')
class _(JsonErrView):

    def get(self):
        captcha = {}
        key, token, b64img = captcha_new()
        captcha['key'] = key
        captcha['img'] = b64img
        self.finish(captcha)


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


@route("/send_captcha")
class SendCaptcha(JsonErrView):

    def post(self):
        err = JsOb()
        email = self.json.email
        if not email:
            err.email = 'Email not found!'

        code_list = random.sample(range(10), 6)
        captcha_code = ''.join(map(str, code_list))
        email_data = dict(
            email_server=EMAIL.get('email_server'),
            email_server_port=EMAIL.get('email_server_port'),
            username=EMAIL.get('user_name'),
            password=EMAIL.get('password'),
            sender=EMAIL.get('sender'),
            receiver=email,
            msg=dict(
                text=captcha_code,
                subject='PingStart Captcha for reset password',
            ),
        )

        send_status = send_email(email_data)
        if send_status != True:
            err.send_status = send_status
        else:
            cpatcha = Captcha.create(email=email, captcha_code=captcha_code)
        self.render(err)


@route("/verify_captcha")
class VerifyCaptcha(JsonErrView):

    def post(self):
        err = JsOb()
        email = self.json.email
        captcha_code = self.json.captcha_code

        if not captcha_code:
            err.captcha_code = u'captcha code can\'t be empty!'

        if not err:
            captcha = Captcha.find_one(dict(email=email, code=captcha_code))
            if not captcha:
                err.captcha_code = u'captcha code not match!'

            elif (datetime.datetime.now() - Tool.str_datetime(captcha.create_time, "%Y-%m-%d %H:%M:%S")).seconds > 300:
                err.captcha_code = u'captcha code expired!'

        self.render(err)


@route("/reset_password")
class ResetPassword(JsonErrView):

    def post(self):
        email = self.json.email
        user = User.find_one(dict(email=email))
        password = self.json.password
        user.password = user.encrypt_pwd(password)
        user.last_update = DateTime().current_time
        user.save()


