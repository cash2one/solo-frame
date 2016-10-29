#!/usr/bin/env python
# coding:utf-8
from _db import redis, R
from solo.captcha import captcha
from b64uuid import b64uuid


R_CAPTCHA = R.CAPTCHA("%s")


def captcha_new():
    token, b64img = captcha()
    key = b64uuid()
    redis.setex(R_CAPTCHA % key, 3600 * 3, token.lower())
    return key, token, b64img


def captcha_verify(key, token):
    if token and (token.lower() == redis.get(R_CAPTCHA % key)):
        captcha_rm(key)
        return True
    return False


def captcha_rm(key):
    redis.delete(R_CAPTCHA % key)

if __name__ == "__main__":
    print(captcha_new()[:2])
    # print(captcha_new())
    pass
