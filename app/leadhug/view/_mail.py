# coding=utf-8
from _base import LoginView,JsonLoginView
from _route import route
from app.leadhug.model.email import EMail
from app.leadhug.model.emodel import EmailModel, EModelNotFound
from app.leadhug.model.offers import Offers
from solo.lib.utils import DateTime


@route('/email')
class EmailList(LoginView):

    def get(self):
        emails = EMail._query(user_id=self.current_user_id)
        self.render(
            emails=emails
        )

@route('/email/new')
class EmailNew(LoginView):

    def get(self):
        e_models = EmailModel.find({'deleted': False})
        active_traffic_time = DateTime.get_day(6)
        offers = Offers.query(active_traffic_time)
        self.render(
            e_models=e_models,
            offers=offers
        )

@route('/emails/j')
class Email_j(JsonLoginView):
    def post(self):
        limit = int(self.json.limit)
        page = int(self.json.page)
        skip = limit * (page - 1)
        emails = EMail.find(limit=limit,skip=skip,)
        emails_count = EMail.count()
        self.finish(dict(emails_count=emails_count,emails=emails))


@route('/e_model')
class EModel(LoginView):

    def get(self):
        #e_models = EmailModel.find({'deleted': False})
        self.render(
            e_models={}
        )

@route('/e_model/j')
class EModel_j(JsonLoginView):
    def post(self):
        limit = int(self.json.limit)
        page = int(self.json.page)
        skip = limit * (page - 1)
        models = EmailModel.find({"deleted":False},limit=limit,skip=skip,)
        models_count = EmailModel.count({"deleted":False})
        self.finish(dict(models_count=models_count,models=models))


@route('/e_model/create')
class EModelNew(LoginView):

    def get(self):
        self.render()
