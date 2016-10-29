#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import LoginView
from app.leadhug.model.user import User
from app.leadhug.model.role import Role


@route('/users')
class UserList(LoginView):
    def get(self):
        self.render()


if __name__ == '__main__':
    pass
