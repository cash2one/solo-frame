#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import sys
import httplib
import traceback
from os.path import join
import tornado
import tornado.web
from tornado.httpclient import HTTPError
from solo.config import APP, DEBUG


def get_error_html(self, status_code, **kwargs):
    if status_code == 404:
        from solo.web.render import render as _render
        path = join(APP, 'base/error/404.html')
        html = _render(path)
        return self.write(html)
    if self.settings.get('debug') and ('exc_info' in kwargs or 'exception' in kwargs):
        # in debug mode, try to send a traceback
        self.set_header('Content-Type', 'text/plain')
        for line in traceback.format_exception(*sys.exc_info()):
            self.write(line)
    else:
        message = kwargs.get('message', httplib.responses[status_code])
        html = '<html><title>%(code)s: %(message)s</title><body>%(code)s: %(message)s</body></html>' % {
            'code': status_code,
            'message': message,
        }
        self.write(html)
#    if not self._finished:
#        self.finish()

tornado.web.RequestHandler.get_error_html = get_error_html

RequestHandler = tornado.web.RequestHandler


class View(RequestHandler):

    def prepare(self):
        super(View, self).prepare()

    def decode_argument(self, value, name=None):
        return value

    def redirect(self, url, permanent=False):
        """Sends a redirect to the given (optionally relative) URL."""
        if self._headers_written:
            raise Exception('Cannot redirect after headers have been written')
        self.set_status(301 if permanent else 302)
        self.set_header('Location', url)
        self.finish()

    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            # if self.request.method not in ('GET', 'HEAD', 'OPTIONS') and \
            #   self.application.settings.get('xsrf_cookies'):
            #    self.check_xsrf_cookie()
            self.prepare()
            if not self._finished:
                args = [self.decode_argument(arg) for arg in args]
                kwargs = dict((k, self.decode_argument(v, name=k))
                              for (k, v) in kwargs.iteritems())
                if hasattr(self, 'init'):
                    getattr(self, 'init')(*args, **kwargs)
                getattr(self, self.request.method.lower())(*args, **kwargs)
                if self._auto_finish and not self._finished:
                    self.finish()
        except Exception, e:
            self._handle_request_exception(e)

if __name__ == '__main__':
    pass
