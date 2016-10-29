#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import sys
sys.path.append('/home/solodev/workspace/asyncboto')
# from solo.config import AWS
from asyncboto.s3.key import AsyncKey
# from boto.s3.key import Key
# from boto import config
import posixpath
import os
from asyncboto import connect_s3
from tornado import gen


# S3 = boto.connect_s3(AWS.ACCESS_KEY_ID, AWS.ACCESS_KEY)
# S3 = connect_s3(
#     AWS.ACCESS_KEY_ID,
#     AWS.ACCESS_KEY,
#     is_secure=False,
# )


class BUCKET_AUTH:
    PRIVATE = 'private'
    PUBLIC_READ = 'public-read'


class S3Storage():

    def __init__(
            self,
            aws_access_key_id,
            aws_secret_access_key,
            bucket,
            key_prefix='',
            aws_s3_bucket_auth=BUCKET_AUTH.PRIVATE
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket
        self.s3 = connect_s3(
            self.aws_access_key_id,
            self.aws_secret_access_key,
            is_secure=False,
        )
        self.key_prefix = key_prefix
        self.aws_s3_bucket_auth = aws_s3_bucket_auth

    @gen.coroutine
    def connect(self):
        self.bucket = yield self.s3.get_bucket(self.bucket_name)
        raise gen.Return(self)

    def exists(self, name):
        for _ in self.bucket.list(prefix=self._get_key_name(name)):
            return True

        return False

    def _get_key_name(self, name):
        return posixpath.join(self.key_prefix,
                              name.replace(os.sep, "/"))

    @gen.coroutine
    def save(self, name, fp, content_type='application/octet-stream'):
        k = AsyncKey(self.bucket, name)
        k.key = posixpath.join(self.key_prefix, name)
        headers = {
            "Content-Type": content_type
        }
        yield k.set_contents_from_file(
            fp,
            headers=headers,
            policy=self.aws_s3_bucket_auth
        )
        # k.close()
        raise gen.Return(k)


class TestStorage(S3Storage):
    bucket_name = 'solomedia'
    key_prefix = 'test'


if __name__ == '__main__':
    import asyncboto
    print asyncboto.__file__
    pass
