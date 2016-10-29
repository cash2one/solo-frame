#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from solo.web.view import View as _View
from solo.lib.jsob import JsOb
from app.web.model.session import Session
# from app.web.model.ob import Ob
from solo.config import HOST
from app.leadhug.model.user import User
# import robot_detection


class UserDict(JsOb):

    def __nonzero__(self):
        return 0


class View(_View):
    _USER_COOKIE_NAME = "S"

    def get_current_user(self):
        current_user_id = self.current_user_id
        if current_user_id:
            # user = Ob.ob_get(current_user_id)
            user = User.find_one(
                dict(_id=current_user_id, deleted=False))
            if user is not None:
                return user
            self.clear_cookie(self._USER_COOKIE_NAME, domain="." + HOST)
            self.current_user_id = 0
        o = UserDict()
        return o

    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            s = self.get_cookie('S')
            self._current_user_id = _current_user_id = Session.id_by_b64(s)
            if s and not _current_user_id:
                self.clear_cookie('S', domain="." + HOST)
        return self._current_user_id or 0

    @current_user_id.setter
    def current_user_id(self, value):
        self._current_user_id = value


if __name__ == '__main__':
    import sys
    if sys.getdefaultencoding() == 'ascii':
        reload(sys)
        sys.setdefaultencoding('utf-8')
