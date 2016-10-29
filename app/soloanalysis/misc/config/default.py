# coding:utf-8
import _env  # noqa
from solo import config


def prepare(o):
    config.APP = 'pingstart'
    o.APP = 'pingstart'
    config.HOST = 'localhost'

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host="mongodb://mongo:27017"
    )

    config.REDIS_CONFIG = dict(
        host='redis',
        port=6379,
        db=0
    )

    config.PORT_BEGIN = 20021
    config.PROCESS_NUM = 1
    config.SECRET = "something"
    # session过期时间, 单位是天
    config.SESSION_EXPIRE = 30


def finish(o):
    pass


if __name__ == '__main__':
    pass
