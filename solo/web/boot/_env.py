# coding:utf-8
# try:
#    import astoptimizer
# except ImportError:
#    pass
# else:
#    astoptimizer.patch_compile(
#        astoptimizer.Config('builtin_funcs', 'pythonbin')
#    )

import sys
from os.path import dirname, abspath, exists, join

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


PREFIX = dirname(abspath(__file__))


def _():
    global PREFIX
    PWD = abspath(__file__)
    while True and len(PWD) > 1:
        PWD = dirname(PWD)
        if exists(join(PWD, 'solo/web/boot')):
            PREFIX = PWD

    for path in (
        #        join(PREFIX, 'z42/virtualenv.zip'),
        join(PREFIX, 'solo/lib'),
        PREFIX,
    ):
        if path:
            if path in sys.path:
                sys.path.remove(path)
            sys.path.insert(0, path)

    import solo._app_config_
    import solo.config._signal

_()
