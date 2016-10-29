# coding=utf-8
import sys
import os
#from app.new_pingstart.model.network import NetWork

path = os.path.join(os.getcwd(), "../../")
sys.path.append(path)
import _env  # noqa
from app.new_pingstart.model import GidKey
from app.web.model._db import redis, R


def data_init():
    for redis_key in GidKey.__dict__.values():
        redis.set(R.GID(redis_key), 1000)

if __name__ == '__main__':
    # data_init()
    redis.incr(R.GID(GidKey.api_key), 10000)
