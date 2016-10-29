# coding:utf-8

from _route import route
from _base import JsonLoginView, LoginView
from app.affiliateleadhug.model.postback import PostBack as PBack, PostBackNotFound
from solo.lib.jsob import JsOb


@route('/postback')
class PostBack(LoginView):

    def get(self):
        self.render()


@route('/post_back/create')
class Create(JsonLoginView):

    def post(self):
        err = JsOb()
        url = self.json.url
        res = PBack.add(self.current_user_id, url)

        if not res:
            err.save = u'save url=%s failure' % url

        self.render(err)


@route('/post_backs')
class PostBacks(JsonLoginView):

    def get(self):
        user_id = self.current_user_id
        post_backs = PBack.query(user_id)
        self.finish(dict(post_backs=post_backs))


@route('/post_back/update')
class Update(JsonLoginView):

    def post(self):
        err = JsOb()
        post_back_id = self.json._id
        post_back_url = self.json.url
        try:
            res = PBack.update(post_back_id, post_back_url)
        except PostBackNotFound:
            err.update = u'update _id=%s failure' % post_back_id

        self.render(err)


@route('/post_back/delete')
class Delete(JsonLoginView):

    def post(self):
        err = JsOb()
        post_back_id = self.json._id
        res = PBack.delete(post_back_id)
        if not res:
            err.delete = u'delete _id=%s failure' % post_back_id
        self.render(err)
