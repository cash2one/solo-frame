#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from solo.web.view import View
from solo.web.render import render
import css
import js


BaseView = View


class View(BaseView):

    def render(self, template_name=None, **kwds):
        if not self._finished:
            if template_name is None:
                if not hasattr(self, 'template'):
                    path = self.__module__.split('.')
                    path.pop(0)
                    path.pop(1)  # 原来的第3个
                    self.template = '/%s/%s.html' % (
                        '/'.join(path),
                        self.__class__.__name__
                    )
                template_name = self.template
            kwds['request'] = self.request
            kwds['this'] = self
            kwds['css'] = css
            kwds['js'] = js
            # kwds['current_user'] = self.current_user
            # kwds['current_user_id'] = self.current_user_id
            self.finish(render(template_name, **kwds))


# class UserDict(JsOb):

#     def __nonzero__(self):
#         return 0


# class CookieView(View):
#     '''没测试, 先别用.
#     '''
#     _USER_COOKIE_NAME = "S"

#     def get_current_user(self):
#         current_user_id = self.current_user_id
#         if current_user_id:
#             # user = Ob.ob_get(current_user_id)
#             user = User.find_one(
#                 dict(_id=current_user_id, status=USER_STATUS.NORMAL))
#             if user is not None:
#                 return user
#             self.clear_cookie(self._USER_COOKIE_NAME, domain="." + HOST)
#             self.current_user_id = 0
#         o = UserDict()
#         return o

#     @property
#     def current_user_id(self):
#         if not hasattr(self, '_current_user_id'):
#             s = self.get_cookie('S')
#             self._current_user_id = _current_user_id = Session.id_by_b64(s)
#             if s and not _current_user_id:
#                 self.clear_cookie('S', domain="." + HOST)
#         return self._current_user_id or 0

#     @current_user_id.setter
#     def current_user_id(self, value):
#         self._current_user_id = value


if __name__ == '__main__':
    pass
