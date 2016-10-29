#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import sys
# import tornado
from tornado.web import HTTPError
import traceback
# from tornado.escape import url_unescape, parse_qs_bytes, native_str
from solo.web.view import View
from jsob import StripJsOb, JsOb
import json
from yajl import loads
from solo.config import DEBUG, RESPONSE_CODE
from app.web.controller.error import DictError
from app.web.controller.signature import signature_verify
from enum import IntEnum
import ujson
from tornado.web import gen


def write_error(self, status_code, **kwargs):
    '''回写API类的异常.
    '''
    self.set_header('Content-Type', 'application/json; charset=UTF-8')

    self.finish(
        {
            'code': RESPONSE_CODE.ERROR,
            'message': ''.join(
                traceback.format_exception(
                    *sys.exc_info())) if DEBUG else self._reason
        }
    )


# tornado.web.RequestHandler.write_error = write_error
def map_intenum(data):
    if isinstance(data, IntEnum):
        return data.value
    if isinstance(data, dict):
        return {k: map_intenum(v) for k, v in data.iteritems()}
    if isinstance(data, (list, tuple)):
        return [map_intenum(v) for v in data]
    return data


class CObjectsEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        o = map_intenum(o)
        return super(CObjectsEncoder, self).iterencode(o, _one_shot)

    def default(self, o):
        if isinstance(o, IntEnum):
            return {'__class__': o.__class__.__name__,
                    '__value__': (o.value,)}
        return super(CObjectsEncoder, self).default(o)


class JsonView(View):

    SUPPORTED_METHODS = ('POST', 'GET')

    write_error = write_error

    def prepare(self):
        self.content_type = self.request.headers.get('content-type')
        super(JsonView, self).prepare()

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            # self.prepare()
            try:
                result = self.prepare()
                if result is not None:
                    result = yield result
            except DictError as e:
                self.finish(e.dump())

            if self._prepared_future is not None:
                self._prepared_future.set_result(None)
            if self._finished:
                return

            args = [self.decode_argument(arg) for arg in args]
            kwargs = dict((k, self.decode_argument(v, name=k))
                          for (k, v) in kwargs.iteritems())
            if hasattr(self, 'init'):
                getattr(self, 'init')(*args, **kwargs)
            try:
                method = getattr(self, self.request.method.lower())
                result = method(*args, **kwargs)
                if result is not None:
                    yield result
            except DictError as e:
                # self._handle_request_exception(e)
                self.finish(e.dump())

            if self._auto_finish and not self._finished:
                self.finish()
        except Exception, e:
            # 回写异常, 并结束异常请求.
            self._handle_request_exception(e)

    def render(self, chunk):
        default_response = {
            'code': RESPONSE_CODE.OK,
            'message': 'OK'
        }
        if not chunk:
            chunk = default_response
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        chunk.update(default_response)
        self.finish(chunk)

    def finish(self, chunk={}):
        callback = self.get_argument('callback', None)
        if callback:
            if type(chunk) is dict:
                chunk = ujson.dumps(chunk, ensure_ascii=False)
            chunk = '%s(%s)' % (callback, chunk)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        if isinstance(chunk, dict):
            super(JsonView, self).finish(ujson.dumps(chunk, ensure_ascii=False))
        else:
            super(JsonView, self).finish(chunk)
        # super(JsonView, self).finish(dumps(chunk))
        # super(JsonView, self).finish(json.dumps(chunk))


class JsonPostView(JsonView):

    SUPPORTED_METHODS = ('POST')

    @property
    def json(self):
        if not self.request.body:
            return JsOb()
        try:
            return StripJsOb(
                **loads(self.request.body.decode('utf-8', 'ignore')))
        except ValueError as e:
            raise HTTPError(400, reason="%s, may be bad json" % str(e))
        # elif self.content_tpye == 'application/x-www-form-urlencode':
        #     print url_unescape(self.request.body)
        #     uri_arguments = parse_qs_bytes(
        #         native_str(self.request.body), keep_blank_values=True)
        #     print uri_arguments
        #     pass


class JsonQueryView(JsonView):

    def prepare(self):
        query_ = self.request.query_arguments
        self.query = JsOb(**{k: query_[k][0] for k in query_.iterkeys()})
        super(JsonQueryView, self).prepare()


class JsonSignatureView(JsonPostView):
    '''带有signature校验的view.
    '''
    def prepare(self):
        super(JsonPostView, self).prepare()
        data = loads(self.request.body.decode('utf-8', 'ignore'))
        signature = data.pop('signature', None)
        # debug模式下不校验签名
        if not DEBUG and not signature_verify(data, signature):
            raise HTTPError(403)


if __name__ == '__main__':
    pass
