#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
import sys
from os.path import join, abspath, dirname, exists
from os import walk, mkdir, chmod
from collections import defaultdict
from base64 import urlsafe_b64encode
from hashlib import md5
from glob import glob
from solo.config import DEBUG, CDN, AWS, APP
from extract import extract_map
from mako.template import Template


CSS_IMG2URL = {}
if not DEBUG:
    uploder = CDN.UPLOADER(AWS.ACCESS_KEY_ID, AWS.ACCESS_KEY, AWS.BUCKET,
                           prefix=APP)
else:
    class uploder:

        @classmethod
        def upload(*args, **kwargs):
            return


BULID = '/tmp/%s' % CDN.HOST
BULID_EXIST = set(glob(BULID + '/*'))
PATH2HASH = {}
if not exists(BULID):
    mkdir(BULID)
    chmod(BULID, 0777)


def css_remove_background_url(path, css):
    dirpath = dirname(path[len(_env.PREFIX):])

    def _(img_url):
        if 'data:image' in img_url or img_url.strip('\'")').endswith('.css'):
            return img_url

        img_url = img_url.replace("'", '').replace('"', '')
        img_url = img_url[4:-1].strip()
        if not (img_url.startswith('https://') or img_url.startswith('http://')
                ):
            if not img_url.startswith('/'):
                img_url = join(dirpath, img_url)
            if img_url in CSS_IMG2URL:
                print img_url, CSS_IMG2URL[img_url]
                img_url = CSS_IMG2URL[img_url]
            elif img_url.startswith('//'):
                pass
            elif not exists(join(BULID, img_url)):
                raise Exception('css error : %s\n%s not exist' %
                                (path, img_url))
        return 'url(%s)' % img_url
    css = extract_map('url(', ')', css, _)
    css = extract_map("url(\"", "\")", css, _)
    css = extract_map("url('", "')", css, _)
    return css


def upload(real_path, md5, suffix, relative_path):
    uploder.upload(real_path, md5, suffix, relative_path)


def run(suffix):
    file_list, merge_list = dirwalk(suffix)
    file_set = set(file_list)

    for i in file_set:
        base = join(_env.PREFIX, suffix)
        with open(i) as infile:
            md5 = hash_name(infile.read(), i)
            print "%s \t %s" % (i, md5)
            # path = join(BULID, hash) + '.' + suffix
            uploder.upload(i, md5, suffix, i.split(base + '/')[1])


def hash_name(content, path):
    hash = urlsafe_b64encode(md5(content).digest()).rstrip('=')
    PATH2HASH[path] = hash
    return hash


def merge_conf(file, base):
    ft = defaultdict(list)
    p = None
    dirpath = dirname(file)
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line[0] == '/':
                path = base + line
            else:
                path = join(dirpath, line)
            if line.endswith(':'):
                p = path[:-1].strip()
            elif line and p:
                ft[p].append(path)
    return ft


def dirwalk(dirname):
    base = join(_env.PREFIX, dirname)
    merge = []
    file = []
    suffix = '.%s' % dirname
    for dirpath, dirnames, filenames in walk(base, followlinks=True):
        for i in filenames:
            path = abspath(join(dirpath, i))
            # if i == 'merge.conf':
            #     merge.append((path, merge_conf(path, base)))
            if i.endswith(suffix):
                # 处理css文件和js文件
                file.append(path)
            # TODO 处理图片文件
            # elif dirname == 'css':
            #     # 处理图片文件
            #     filesuffix = splitext(path)[-1][1:]
            #     if filesuffix not in ('py', 'pyc', 'orig', 'swp', 'conf',
            #                           'txt', 'rst', 'html'):
            #         url = path[len(_env.PREFIX):]
            #         with open(path, 'rb') as infile:
            #             filemd5 = urlsafe_b64encode(
            #                 md5(infile.read()).digest()).rstrip('=')
            #             CSS_IMG2URL[url] = filemd5
            #             cache_path = join(BULID, filemd5)
            #             if not exists(cache_path) and not DEBUG:
            #                 print 'upload %s > //%s/%s' % (
            #                     url, CDN.HOST, filemd5)
            #                 print _env.PREFIX
            #                 upload(join(_env.PREFIX, url[1:]), filemd5, suffix, i)
            #                 # r = CDN.upload(filemd5, path)
            #                 _hash = filemd5
            #                 if _hash:
            #                     with open(cache_path, 'w') as c:
            #                         c.write(_hash)
    return file, merge


def write_hash():
    init = defaultdict(list)
    for file_name, hash in PATH2HASH.iteritems():
        suffix, file_name = file_name[len(_env.PREFIX) + 1:].split('/', 1)
        init[suffix].append((file_name.rsplit('.', 1)[0], hash))

    for suffix, flist in init.iteritems():
        with open(join(_env.PREFIX, 'solo/web/boot/hash.py.mako')) as tlp_file:
            tlp = tlp_file.read()
        template = Template(tlp)
        with open(join(_env.PREFIX, suffix, '_hash_.py'), 'w') as hash_file:
            hash_file.write(
                template.render(
                    file_list=flist
                )
            )

run('css')
run('js')
write_hash()
sys.exit(0)
