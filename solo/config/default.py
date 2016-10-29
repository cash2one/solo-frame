# coding:utf-8
import _env  # noqa


def prepare(o):
    o.DEBUG = True

    o.PORT = 8942

    class WEBSET:
        TITLE = 'A tornado warp from NewBornTown.inc'
        KEYWORDS = 'NewBornTown,Solo'
        DESCRIPTION = 'Be solo and awesome'

    o.WEBSET = WEBSET

    class MONGO:
        DBNAME = 'dbname'
        HOST = 'host'
        USER = 'user'
        PORT = 'port'
        PASSWORD = 'password'
    o.MONGO = MONGO
    o.DBNAME = "solofream"

    class RESPONSE_CODE:
        OK = 1
        ERROR = 2
    o.RESPONSE_CODE = RESPONSE_CODE

    # 随机自增量因数
    o.RANDOM_GID_FACTOR = 20

    class AWS:
        ACCESS_KEY_ID = ''
        ACCESS_KEY = ''
        REGION = 'us-east-1'
        BUCKET = ''

    o.AWS = AWS

    class CDN:
        HOST = 'localhost'
        UPLODER = None

    o.CDN = CDN
