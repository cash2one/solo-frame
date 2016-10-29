#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from solo.web.route import Route
from solo.config import HOST

route = Route(host=HOST.replace(".", "\\."))

ROUTE_LIST = [route]
