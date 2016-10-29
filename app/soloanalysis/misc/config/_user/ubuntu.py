import _env  # noqa
from solo import config


def prepare(o):
    config.APP = 'soloanalysis'
    o.APP = 'soloanalysis'
    config.HOST = 'analysis1.com'

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host="mongodb://127.0.0.1:27017"
    )

    config.REDIS_CONFIG = dict(
        host='localhost',
        port=6379,
        db=0
    )
    config.PORT_BEGIN = 20021
    config.PROCESS_NUM = 1
    config.DBNAME = 'analysis'
