#!/usr/bin/env python
# coding:utf-8


class BaseControllerError(BaseException):
    pass


class DictError(BaseException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def dump(self):
        return {"code": self.code, "message": self.message}
