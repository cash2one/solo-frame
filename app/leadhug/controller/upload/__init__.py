#!/usr/bin/env python
# coding=utf-8
from tornado import gen
import _env  # noqa
import boto.s3.connection
from solo.config import AWS


class StorageS3(object):

    def __init__(self):
        self.conn = boto.connect_s3(
            aws_access_key_id=AWS.ACCESS_KEY_ID,
            aws_secret_access_key=AWS.ACCESS_KEY,
            is_secure=False,
            # calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
        self.bucket_name = AWS.BUCKET_UPLOAD

    def get_bucket(self):
        self.bucket = self.conn.get_bucket(self.bucket_name)
        self.bucket.set_acl('public-read')
        return self.bucket


if __name__ == '__main__':
    s = StorageS3()
    bucket = s.conn.get_bucket('leadhugstatic')
    print bucket.get_key('test2.log').generate_url(expires_in=1000)
    print dir(bucket)
