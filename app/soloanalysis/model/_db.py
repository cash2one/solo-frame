#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import redis as _redis
from solo.config import REDIS_CONFIG
from redis_key import RedisKey

redis = _redis.StrictRedis(**REDIS_CONFIG)

R = RedisKey(redis)

if __name__ == '__main__':
    # from redis_key import REDIS_KEY_ID,REDIS_ID_KEY
    # for i in redis.hgetall(REDIS_ID_KEY).iteritems():
    #     print i
    # print REDIS_CONFIG
    # print redis.get(R.ICO_URL("%s")%100000011)
    pass
