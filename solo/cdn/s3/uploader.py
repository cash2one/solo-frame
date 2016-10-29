#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from boto import connect_s3
from boto.s3.key import Key
from solo.cdn import CDN


class S3(CDN):

    # def __init__(self):
    def __init__(self, aws_key_id, aws_key, aws_bucket, prefix=''):
        self.conn = connect_s3(
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_key,
        )
        self.bucket = self.conn.get_bucket(aws_bucket)
        super(S3, self).__init__(prefix=prefix)

    def do_upload(self, real_path, upload_path):
        print 'uploading %s to %s' % (real_path, upload_path)
        key = Key(self.bucket, name=upload_path)
        key.set_contents_from_filename(real_path, policy="public-read")
        key.close()

    def exists(self, server_path, md5):
        key = Key(self.bucket, name=server_path)
        return key.exists()


if __name__ == '__main__':
    s3 = S3(
        'AKIAJBA3U35J6A7G3U5Q',
        'L86Sn+yuLQdVOkcC7uigFQDbIkmfLAlHjeoae7x2',
        'solomedia'
    )
    print list(s3.bucket.list())
    pass
