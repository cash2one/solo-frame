#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from os.path import join, dirname


class CDN(object):

    def __init__(self, prefix=''):
        self.prefix = prefix

    def upload(self, real_path, md5, suffix, file_name, force=False):
        """upload

        :param real_path: 要上传文件的绝对路径
        :param file_md5: 文件的MD5值
        :param suffix: 文件类型(css, js)
        :param file_name: 文件名称(包含项目中路径, 例如liveadmin/test.css)
        :param prefix: 上传文件路径前缀
        :param force: 强制上传
        """
        server_path = join(self.prefix, suffix, dirname(file_name), md5)
        if not force and self.exists(server_path, md5):
            print 'file %s exixted pass' % real_path
            return
        self.do_upload(real_path, server_path)

    def exists(self, server_path, md5):
        raise NotImplementedError()

    def do_upload(self, real_path, upload_path):
        raise NotImplementedError()

    def remove(self, *args, **kwargs):
        raise NotImplementedError()
