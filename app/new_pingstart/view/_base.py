# coding:utf-8
import _env  # noqa
from tornado.web import HTTPError
from app.web.model.session import Session
from solo.web.render import render
from app.new_pingstart.view._user import View as _View
from app.new_pingstart.view.base import View as BaseView
from jsob import JsOb, StripJsOb
from solo.config import HOST, SESSION_EXPIRE
from yajl import loads, dumps
import js
import css


class View(_View):

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
            # current_user = self.current_user
            kwds['request'] = self.request
            kwds['this'] = self
            kwds['css'] = css
            kwds['js'] = js
#            kwds['_xsrf'] = self._xsrf
            kwds['current_user'] = self.current_user
            kwds['current_user_id'] = self.current_user_id
            #           kwds['_T'] = _T
            self.finish(render(template_name, **kwds))


class JsonView(_View):

    @property
    def json(self):
        if self.request.method == "POST":
            body = self.request.body
        else:
            body = self.get_argument('o')
        return StripJsOb(**loads(body.decode('utf-8', 'ignore')))

    def render(self, chunk):
        if not chunk:
            chunk = '{}'
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        super(JsonView, self).finish(chunk)


class JsonErrView(BaseView):
    '''封装了错误提示的View.
    '''

    @property
    def json(self):
        '''将request.body转换成了JsOb.
        '''
        if self.request.method == "POST":
            body = self.request.body
        else:
            body = self.get_argument('o')
        return StripJsOb(**loads(body.decode('utf-8', 'ignore')))

    def render(self, chunk):
        if chunk:
            if type(chunk) is dict:
                chunk = dumps(chunk)
            chunk = '{"err":%s}' % chunk
        else:
            chunk = '{}'
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(chunk)

    def finish(self, chunk={}):
        callback = self.get_argument('callback', None)
        if callback:
            if type(chunk) is dict:
                chunk = dumps(chunk)
            chunk = '%s(%s)' % (callback, chunk)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        super(JsonErrView, self).finish(chunk)


class JsonLoginView(_View, JsonErrView):
    '''
        login session auth
    '''
    def prepare(self):
        if not self.current_user_id:
            self.redirect('/logout')
        else:
            session = Session.new(self.current_user_id)
            self.set_cookie('S', session, domain="." + HOST, expires_days=SESSION_EXPIRE)


class LoginView(View):
    '''登录认证
    '''
    def prepare(self):
        if not self.current_user_id:
            self.redirect('/logout')
        else:
            session = Session.new(self.current_user_id)
            self.set_cookie('S', session, domain="." + HOST, expires_days=SESSION_EXPIRE)


class JsonQueryView(JsonView):
    def prepare(self):
        if self.request.method == 'GET':
            query_ = self.request.query_arguments
            self.query = JsOb(**{k: query_[k][0] for k in query_.iterkeys()})
        super(JsonQueryView, self).prepare()
