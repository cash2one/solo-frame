# coding:utf-8
import _env  # noqa
import sys
from solo.web import cgi
import tornado.web


def main(route, port):
    if len(sys.argv) != 1 and sys.argv[1][:6] == '--port':
        port = sys.argv[1].rsplit('=')[1]

    print 'SERVE ON PORT %s' % port
    application = cgi.application(route, tornado.web.Application)
    application.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    # ioloop.set_blocking_log_threshold(0.2)
    ioloop.start()


if __name__ == '__main__':
    from solo.config import APP, HOST, PORT_BEGIN
    from importlib import import_module
    from app.web.view._route import ROUTE_LIST as WEB_ROUTE_LIST
    print HOST
    __import__('app.%s.view._url' % APP)
    __import__('app.web.view._url')
    ROUTE_LIST = import_module('app.%s.view._route' % APP).ROUTE_LIST
    ROUTE_LIST += WEB_ROUTE_LIST
    main(reversed(ROUTE_LIST), PORT_BEGIN)
