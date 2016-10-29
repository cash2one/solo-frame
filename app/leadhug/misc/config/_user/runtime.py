import _env  # noqa
from solo import config
from solo.cdn.s3.uploader import S3
import os


def prepare(o):
    config.APP = 'leadhug'
    config.DEBUG = False
    o.APP = 'leadhug'
    config.HOST = os.getenv("VIRTUAL_HOST", 'testadmin.leadhug.com')
    config.SESSION_EXPIRE = 1
    config.PORT_BEGIN = 20000
    config.PROCESS_NUM = 1
    config.SECRET = "bwxnHjAYsPC52iuWZn09"
    

    config.MONGO_CONFIG = dict(
        # host="mongodb://<user>:<password>@<host>:<port>"
        host=os.getenv("AFFILIATE_MONGO", "mongodb://10.1.5.102:27017"),
        slave_okay=True
    )
    config.DBNAME = 'leadhug'

    config.REDIS_CONFIG = dict(
        host='redis',
        port=6379,
        db=0
    )

    config.AWS.ACCESS_KEY_ID = 'AKIAJRRTI7UMYVNY56DQ'
    config.AWS.ACCESS_KEY = 'S7xuo6xzgYwMema7ThL+P46a8wwB9bt5Q81a59r+'
    config.AWS.REGION = 'us-east-1'
    config.AWS.BUCKET = 'adplatformstatis'
    config.AWS.BUCKET_UPLOAD = 'leadhugstatic'

    config.CDN.HOST = "s3-us-west-2.amazonaws.com"
    config.CDN.PREFIX = 'adplatformstatis'
    config.CDN.UPLOADER = S3

    config.GEARMAN_SERVER = ['gearman']
    config.GEARMAN_CLIENT = dict(
        email_server='smtp.gmail.com',
        email_server_port=25,
        sender='support@leadhug.com',
        user_name='support@leadhug.com',
        password='leadhug123',
        worker='email',
    )
