#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import View, LoginView
from solo.config import HOST
from app.web.model.session import Session


@route('/')
class Index(LoginView):
    def get(self):
        self.redirect('/report')


@route('/login|/index')
class Login(View):
    def get(self):
        self.redirect('/')


@route('/signup')
class SignUp(View):
    def get(self):
        self.render()


@route('/logout')
class Logout(View):
    def get(self):
        if self.current_user_id:
            self.clear_cookie('S', domain="." + HOST)
            Session.rm(self.current_user_id)
        self.render('/new_pingstart/login/Login.html')


@route("/find_password")
class ForgetPassword(View):

    def get(self):
        email = self.get_argument('email', None, strip=True)
        self.render(email=email)


if __name__ == '__main__':
    pass
