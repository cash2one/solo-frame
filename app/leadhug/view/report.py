# coding=utf-8
from _base import LoginView
from _route import route
from solo.lib.utils import DateTime


@route('/report')
class Report(LoginView):

    def get(self):
        end = DateTime.get_day(1)
        start = DateTime.get_day(7)
        self.render(start=start, end=end)

if __name__ == '__main__':
    pass
