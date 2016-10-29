# coding:utf-8
import _env  # noqa
from solo.config import DEBUG, CDN, APP
from os.path import dirname, basename, join

__HASH__ = {
    % for name, hash in file_list:
    "${name}": '${hash}',  # ${name.rsplit('.', 1)[0].replace('.', '_').replace('-', '_').replace('/', '_')}
    % endfor
}

__vars__ = vars()


def _():
    for file_name, hash in __HASH__.iteritems():

        if DEBUG:
            suffix = basename(dirname(__file__))
            value = "/%s/%s.%s" % (suffix, file_name, suffix)
        else:
            suffix = basename(dirname(__file__))
            value = "//%s/%s" % (CDN.HOST, join(CDN.PREFIX, APP, suffix, dirname(file_name), hash))

        name = file_name.replace('.', '_').replace('-', '_').replace('/', '_')

        __vars__[name] = value

_()

del __vars__["_"]
