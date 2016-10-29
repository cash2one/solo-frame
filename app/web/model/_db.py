#!/usr/bin/env python
# coding:utf-8
import _env  # noqa

import redis as _redis
from solo.config import REDIS_CONFIG
from redis_key import RedisKey

redis = _redis.StrictRedis(**REDIS_CONFIG)

R = RedisKey(redis)
# from solo.web.mongo import Doc


if __name__ == '__main__':
    print REDIS_CONFIG
    print redis.get(R.ICO_URL("%s") % 100000011)
    from pprint import pprint
    print pprint(redis.info())
