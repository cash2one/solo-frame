#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import View, LoginView, JsonLoginView
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.role import Role
from solo.config import HOST, SESSION_EXPIRE
from app.web.model.session import Session
from solo.lib.jsob import JsOb
from solo.lib.utils import is_email, is_valid_password
from yajl import loads
from app.leadhug.model.user import User


@route('/')
class index(LoginView):

    def get(self):
        self.redirect('/report')


@route('/login|/index')
class login(View):

    def _session_new(self, account, user_id):
        session = Session.new(user_id)
        self.set_cookie('S', session, domain="." + HOST,
                        expires_days=SESSION_EXPIRE)
        self.set_cookie('E', account, domain="auth." +
                                             HOST, expires_days=SESSION_EXPIRE)

    def get(self):
        self.render()

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = User.find_one(dict(email=email, password=password))
        if user:
            affiliate = Affiliate.find_one(dict(user_id=int(user._id)))
            if affiliate:
                if affiliate.status == '1':
                    self._session_new(email, user._id)
                    self.redirect('/report')


@route('/logout')
class Logout(LoginView):

    def get(self):
        if self.current_user_id:
            self.clear_cookie('S', domain="." + HOST)
            Session.rm(self.current_user_id)
        self.redirect('/')


@route("/account/signup")
class Signup(View):

    def get(self):
        self.render()


@route('/account')
class Account(LoginView):

    def get(self):
        user_id = int(self.current_user_id)
        account = Affiliate.find_one(dict(user_id=user_id))
        user = User.find_one(dict(_id=user_id))
        account['name'] = user.account
        account['email'] = ';'.join(user.email)
        account['password'] = user.password
        account['phone'] = user.phone
        account['createdTime'] = user.createdTime
        account['last_login'] = user.last_login
        account['skype_id'] = user.skype_id
        self.render(account=account)


@route('/account/modify')
class AccountModify(LoginView):

    def get(self):
        user_id = int(self.current_user_id)
        account = Affiliate.find_one(dict(user_id=user_id))
        user = User.find_one(dict(_id=user_id))
        account['name'] = user.account
        account['email'] = ';'.join(user.email)
        account['password'] = user.password
        account['phone'] = user.phone
        account['createdTime'] = user.createdTime
        account['last_login'] = user.last_login
        account['skype_id'] = user.skype_id
        self.render(account=account)


@route('/j/account/save')
class AccountUpdate(JsonLoginView):

    def post(self):
        form = loads(self.request.body)
        err = JsOb()
        user = self.current_user
        if not form.get('email'):
            err.email = 'Please input email'
        else:
            emails = form['email'].replace(' ', '').split(';')
            for e in emails:
                if not is_email(e):
                    err.email = 'Email not valid, email=%s' % e
                elif e not in user.email and User.count(dict(email=e, deleted=False)):
                    err.email = "email %s already be used!" % e

        if not form.get('name'):
            err.name = 'Pleast input your name'
        elif form.get('name') != user.account and User.count(dict(account=form.get('name'), deleted=False)):
            err.name = 'name already be used!'

        if not form.get('password'):
            err.password = 'Please input password'
        elif form.get('password') != user.password and not is_valid_password(form.get('password')):
            err.password = 'Password not valid'
        if not err:
            user = User._update_account(form.get('user_id'), **dict(
                email=form.get('email').replace(' ', '').split(';'),
                password=form.get('password'),
                account=form.get('name'),
                skype_id=form.get('skype_id'),
                phone=form.get('phone'),
                role_id=Role.affiliate()._id
            ))
            Affiliate._update(form.get('_id'), **form)
        self.render(err)

if __name__ == '__main__':
    pass
