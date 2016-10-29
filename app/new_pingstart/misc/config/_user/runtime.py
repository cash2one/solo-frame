import _env  # noqa
import os
import time
from solo import config
from solo.cdn.s3.uploader import S3


def prepare(o):
    config.APP = 'new_pingstart'
    o.APP = 'new_pingstart'
    config.DEBUG = False
    config.HOST = os.getenv('PS_VIRTUAL_HOST', 'new_pingstart.com')
    config.SESSION_EXPIRE = 30
    config.PORT_BEGIN = 20000
    config.PROCESS_NUM = 1
    config.SECRET = "has89-a9=af0=q2e21-931^*&5d8qdq8wd2"

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host=os.getenv("PS_MONGO", "mongodb://10.1.5.102:27017")
    )
    config.DBNAME = 'new_pingstart'

    config.REDIS_CONFIG = dict(
        host=os.getenv('PS_REDIS', 'redis') ,
        port=6379,
        db=0
    )

    config.EMAIL = dict(
        email_server='smtp.qq.com',
        email_server_port=587,
        sender='769990688@qq.com',
        user_name='769990688@qq.com',
        password='asdfgvcxz',
    )

    config.AWS.ACCESS_KEY_ID = 'AKIAJRRTI7UMYVNY56DQ'
    config.AWS.ACCESS_KEY = 'S7xuo6xzgYwMema7ThL+P46a8wwB9bt5Q81a59r+'
    config.AWS.REGION = 'us-east-1'
    config.AWS.BUCKET = 'adplatformstatis'

    config.CDN.HOST = "s3-us-west-2.amazonaws.com"
    config.CDN.PREFIX = 'adplatformstatis'
    config.CDN.UPLOADER = S3