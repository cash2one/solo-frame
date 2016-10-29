#!/usr/bin/env python
# coding:utf-8

from _db import redis, R
from os import urandom
import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode
from solo.config import SESSION_EXPIRE

R_SESSION = R.SESSION('%s')


class Session(object):

    @classmethod
    def id_by_b64(cls, session):
        id, binary = _id_binary_decode(session)
        if id:
            key = R_SESSION % id
            id = int(float(id))
            if id and binary and binary == redis.get(key):
                return id

    @classmethod
    def new(cls, id, expire=SESSION_EXPIRE * 3600 * 24):
        id = int(float(id))
        if id:
            key = R_SESSION % id
            s = redis.get(key) or urandom(12)
            redis.setex(key, expire, s)
            return _id_binary_encode(id, s)

    @classmethod
    def rm(cls, id):
        redis.delete(R_SESSION % id)


def _id_binary_decode(session):
    if not session:
        return None, None
    id, value = session.split('.', 1)
    try:
        value = urlsafe_b64decode(value)
    except (binascii.Error, TypeError):
        return None, None
    id = int(id)
    return id, value


def _id_binary_encode(id, session, encode=urlsafe_b64encode):
    ck_key = encode(session)
    return '%s.%s' % (id, ck_key)


if __name__ == '__main__':
    # s = Session.new(1)
    # print s
    # print Session.id_by_b64(s)
    id = 12907758
    key = R_SESSION % id
    redis.delete(key)
