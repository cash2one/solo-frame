import _env  # noqa
from solo import config


def prepare(o):
    config.DEBUG = True
    config.APP = 'new_pingstart'
    o.APP = 'new_pingstart'
    config.HOST = 'new_pingstart.com'

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host="mongodb://127.0.0.1:27017"
    )
    config.DBNAME = 'new_pingstart'
    config.REDIS_CONFIG = dict(
        host='localhost',
        port=6379,
        db=0
    )
    config.PORT_BEGIN = 20021
    config.PROCESS_NUM = 1
