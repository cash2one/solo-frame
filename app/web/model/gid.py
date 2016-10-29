#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from app.web.model._db import redis, R
import random
from solo.config import RANDOM_GID_FACTOR

R_GID = R.GID('%s')

# if not redis.exists(R_GID):
#     redis.set(R_GID, 9912499)


def gid(key):
    return redis.incr(R_GID % key)


def random_incr_gid(key):
    return redis.incrby(R_GID % key, random.randint(1, RANDOM_GID_FACTOR))

def init_gid(key, value):
    redis.set(R_GID % key, value)

if __name__ == '__main__':
    pass
