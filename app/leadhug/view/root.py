#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import View, LoginView
from solo.config import HOST
from app.web.model.session import Session


@route('/')
class index(LoginView):
    def get(self):
        user = self.current_user
        if user._role != 'Finance':
            self.redirect('/report')
        else:
            self.redirect('/invoices')


@route('/login|/index')
class login(View):
    def get(self):
        self.render()


@route('/logout')
class Logout(View):
    def get(self):
        if self.current_user_id:
            self.clear_cookie('S', domain="." + HOST)
            Session.rm(self.current_user_id)
        self.redirect('/')
        self.render()


if __name__ == '__main__':
    pass
