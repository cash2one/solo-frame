#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from hashlib import md5
from solo.config import SECRET
import json


def signature_verify(data, signature, secret=SECRET):
    return signature == make_signature(data, secret=SECRET)


def make_signature(data, secret=SECRET):
    # FIXME: 并不支持JSON嵌套的情况
    '''计算给定数据的签名.

    将data进行urlencode, 按&切割后升序排序, 加上密钥算一个md5值并返回.
    注意, 并不支持json嵌套的情况.

    :param data:
    :param secret:
    '''
    args = []
    for key, value in data.items():
        args.append("%s=%s" % (key,
                               json.dumps(
                                   value,
                                   ensure_ascii=False,
                                   separators=(',', ':')
                               )
                               ))
    args = sorted(args)
    unsign_str = "&".join(args)
    m = md5()
    m.update(unsign_str)
    m.update(secret)
    return m.hexdigest()

if __name__ == '__main__':
    data = {
          "openid": 2,
          "username": "200300031",
          "platform": 0
    }
    print '"signature": "%s"' % make_signature(data, SECRET)
    print json.dumps(data)
