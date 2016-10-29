#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
# from solo.web.view import View
from solo.storage.file import File
from io import BytesIO
from os.path import splitext, join
import hashlib
from tornado.web import RequestHandler
from tornado import gen
from tornado.web import asynchronous
from solo.storage.s3_storage import S3Storage, BUCKET_AUTH
from solo.config import AWS
from utils import is_valid_path


# S3_STORAGE = S3Storage(
#     AWS.ACCESS_KEY_ID,
#     AWS.ACCESS_KEY,
#     AWS.BUCKET,
#     aws_s3_bucket_auth=BUCKET_AUTH.PUBLIC_READ,
# )


class MultipartFileUploadView(RequestHandler):

    SUPPORTED_METHODS = ('POST')

    def prepare(self):
        upload_file = self.request.files['file'][0]
        self.file_content = upload_file['body']
        self.file_content_type = upload_file['content_type']
        self.filename = upload_file['filename']
        file_path = self.request.body_arguments.get('path', ['/upload'])[0]
        if is_valid_path(file_path):
            self.file_path = file_path
        else:
            self.finish({'Error': 'file path not valid, path: %s' % file_path})
            return
        self.file_ext = splitext(self.filename)[1]
        content_bytes = BytesIO(self.file_content)
        f_md5 = hashlib.md5(self.file_content).hexdigest()
        self.upload_path = join(self.file_path,
                                '%s%s' % (f_md5, self.file_ext))
        self.upload_file = File(content_bytes, name=join(
            self.file_path,
            '%s%s' % (f_md5, self.file_ext)))

    @asynchronous
    def post(self):
        self.upload()

    @asynchronous
    @gen.coroutine
    def upload(self, callback=None):
        s3_storage = S3Storage(
            AWS.ACCESS_KEY_ID,
            AWS.ACCESS_KEY,
            AWS.BUCKET,
            aws_s3_bucket_auth=BUCKET_AUTH.PUBLIC_READ,
        )
        yield s3_storage.connect()
        try:
            key = yield s3_storage.save(
                self.upload_path,
                self.upload_file,
                content_type=self.file_content_type
            )
            self.uploaded(key)
        except Exception as e:
            import traceback
            import sys
            traceback.format_exception(
                *sys.exc_info())
            print e

    def uploaded(self, key):
        raise NotImplementedError('Not implemented')
