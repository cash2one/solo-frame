# coding:utf-8
import _env  # noqa
from _route import route
from app.leadhug.controller.tools import DateTime
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.role import Role
from app.leadhug.view._base import JsonErrView, JsonLoginView
from app.leadhug.model.user import User, UserNotFoundError, \
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

        if not self.json.login_from:
            if not self.json.captcha_code:
                err.captcha_code = 'Please input captcha code'
            elif not captcha_verify(self.json.captcha_key, self.json.captcha_code):
                err.captcha_code = 'captcha code incorrect'

        if not err:
            try:
                if not self.json.login_from:
                    user = User.verify(self.json.email, self.json.password)
                else:
                    user = User.find_one(
                        dict(email=self.json.email, password=self.json.password))
                if user:
                    affiliate = Affiliate.find_one(dict(user_id=int(user._id)))
                    if affiliate:
                        if affiliate.status == '1':
                            self._session_new(self.json.email, user._id)
                            user.last_login = DateTime().current_time
                            user.save()
                        else:
                            err.application = 'The Account is Approving....'
                    else:
                        err.email = 'Email not found, Please call the manager!'
            except UserNotFoundError:
                err.email = "email not found"
            except PasswordNotMatchError:
                err.password = "password incorrect"

        self.render(err)


@route('/j/sign')
class Create(JsonErrView):

    def post(self):
        err = JsOb()
        form = self.json

        if not form.email:
            err.email = 'Please input email'
        else:
            emails = form.email.replace(' ', '').split(';')
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

        if form.password != form.confirmPassword:
            err.confirmPassword = 'Entered passwords differ'

        if not form.country:
            err.country = 'Please input Country'

        if not form.company:
            err.company = 'Please input Company'

        if not form.skype_id:
            err.skype = 'Please input Skype ID'

        if not form.phone:
            err.phone = 'Please input Phone'

        if not self.json.captcha_code:
            err.captcha_code = 'Please input captcha code'
        elif not captcha_verify(self.json.captcha_key, self.json.captcha_code):
            err.captcha_code = 'captcha code incorrect'

        if not err:
            kw = dict(
                email=emails,
                password=form.password,
                account=form.account,
                role_id=Role.affiliate()._id,
                skype_id=form.skype_id,
                phone=form.phone,
            )
            user = User._create(**kw)
            payment = {
                'invoice_frequency': '',
                'threshold': '',
                'payment_method': '',
                'beneficiary': '',
                'account_number': '',
                'bank': '',
                'route': '',
                'paypal': ''
            }
            affiliate = Affiliate._save(
                **dict(user_id=int(user._id), country=form.country, status='2', company=form.company, payment=payment))

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


@route("/j/roles")
class Roles(JsonLoginView):

    def get(self):
        roles = Role.find({'_id': {'$ne': 1}})
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
        new_password = User.encrypt_pwd(self.json.new_password)
        self.current_user.password = new_password
        self.current_user._id = int(self.current_user_id)
        self.current_user.save()
        self.finish(dict(res=True))
