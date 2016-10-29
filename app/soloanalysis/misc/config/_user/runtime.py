import _env  # noqa
from solo import config
import os
from solo.cdn.s3.uploader import S3

def prepare(o):
    config.APP = 'affiliateleadhug'
    o.APP = 'affiliateleadhug'
    config.HOST = os.getenv("AFFILIATE_HOST", "testaffiliate.leadhug.com")
    config.DEBUG = False

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host=os.getenv("AFFILIATE_MONGO", "mongodb://10.1.5.102:27017")
    )

    config.REDIS_CONFIG = dict(
        host=os.getenv("AFFILIATE_REDIS", 'redis'),
        port=6379,
        db=0
    )
    config.SESSION_EXPIRE = 1
    config.DBNAME = 'leadhug'
    config.PORT_BEGIN = 20000
    config.PROCESS_NUM = 1
    config.SECRET = "bwxnHjAYsPC52iuWZn09"

    config.AWS.ACCESS_KEY_ID = 'AKIAJRRTI7UMYVNY56DQ'
    config.AWS.ACCESS_KEY = 'S7xuo6xzgYwMema7ThL+P46a8wwB9bt5Q81a59r+'
    config.AWS.REGION = 'us-east-1'
    config.AWS.BUCKET = 'adplatformstatis'

    config.CDN.HOST = "s3-us-west-2.amazonaws.com"
    config.CDN.PREFIX = 'adplatformstatis'
    config.CDN.UPLOADER = S3
