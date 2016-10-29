#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from solo.web.mongo import mongo
import sys

APPNAME = sys.argv[1]
__import__("app.%s.view._url" % APPNAME)

for k, v in mongo._registered_documents.iteritems():
    print "indexing", k
    v.generate_index(v._collection)
