#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env  # noqa
from solo.config import HOST
import getpass
import socket
import re
from mako.template import Template
from os import mkdir
from os.path import join, dirname, exists, isdir, abspath

_CONFIG_DIR = join(abspath(dirname(__file__)), '..')

for name in (

    'nginx',
    'supervisord'

):
    with open(join(dirname(__file__), '%s.conf' % name)) as conf:
        tmpl = conf.read()
    T = Template(tmpl)

    dirpath = join(_CONFIG_DIR, name)
    if not exists(dirpath):
        mkdir(dirpath)
    hostname = socket.gethostname()
    path = join(dirpath, hostname)
    if not exists(path):
        mkdir(path)
    user = getpass.getuser()
    filename = join(path, '%s.conf' % user)
    with open(filename, 'w') as f:
        f.write(T.render(
            hostname=hostname,
            user=user
        ))

    print('created nginx configure files at %s' % path)
