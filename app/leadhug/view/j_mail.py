# coding:utf-8
import datetime
import _env  # noqa
from _route import route
from app.leadhug.controller.tools import DateTime
from app.leadhug.model.affiliates import Affiliate
from app.leadhug.model.offer_affiliate import OfferAffiliate
from app.leadhug.model.offers import Offers
from app.leadhug.model.user import User
from app.leadhug.view._base import JsonLoginView
from solo.lib.jsob import JsOb
from app.leadhug.model.email import EMail
from app.leadhug.model.emodel import EmailModel as EModel, EModelNotFound
from solo.lib.utils import is_email


@route('/j/email')
class Email(JsonLoginView):

    def __init__(self, *args, **kwargs):
        self.err = JsOb()
        super(Email, self).__init__(*args, **kwargs)

    def post(self):
        if self.json.action == 'send':
            res = self.send()
            if not res:
                self.render(self.err)

        if self.json.action == 'query':
            self.query()
        self.render(self.err)

    def send(self):
        content = self.json.content or {}

        if not content.get('receiver'):
            self.err.receiver = u'receiver can\'t be empty!'
        else:
            content['receiver'] = content['receiver'].split(',')
            error_receiver = []
            for email in content['receiver']:
                if not is_email(email):
                    error_receiver.append(email)
            if error_receiver:
                self.err.receiver = u'receiver emails={} is not valid!'.format(error_receiver)

        if not content.get('message'):
            self.err.message = u'message can\'t be empty!'

        if self.err:
            return False
        content['user_id'] = self.current_user_id
        EMail._create(**content)
        return True

    def query(self):
        return EMail._query(self.json.model_id, self.json.limit, self.json.offset)


@route('/j/e_model')
class Emodel(JsonLoginView):

    def __init__(self, *args, **kwargs):
        self.err = JsOb()
        super(Emodel, self).__init__(*args, **kwargs)

    def post(self):

        if not self.json.content:
            self.err.error = u'content can\'t be empty'
            self.render(self.err)

        if self.json.action == 'create':
            self.create()

        if self.json.action == 'query':
            e_model = self.query()
            self.finish(dict(e_model=e_model if e_model else {}))

        if self.json.action == 'delete':
            res = self.delete()
            if not res:
                self.render(self.err)

        if self.json.action == 'update':
            self.update()

    def create(self):

        if not self.json.content:
            self.err.content = u'content can\'t be empty'

        if self.err:
            return False

        EModel._create(**self.json.content)
        return True

    def query(self):
        e_model_id = self.json.content.get('e_model_id')
        if e_model_id:
            return EModel._query(spec=dict(_id=int(e_model_id)))

    def delete(self):
        e_model_id = self.json.content.get('e_model_id')
        if not e_model_id:
            self.err.error = u'e_model can\'t be empty or character'
            return False

        if not self.err:
            return EModel._delete(e_model_id)

    def update(self):
        content = self.json.content.get('content')
        e_model_id = self.json.content.get('e_model_id')
        model_name = self.json.content.get('model_name')
        if not content:
            self.err.error = u'content can\'t be empty or character'

        if not self.err:
            return EModel._update(e_model_id, model_name, content)


@route("/email/receivers")
class GetReceiver(JsonLoginView):

    def get(self):
        pass


@route("/j/email/offers")
class ActiveTrafficOffer(JsonLoginView):

    def get(self):
        active_traffic_time = DateTime.get_day(6)
        offers = Offers.query(active_traffic_time)
        self.finish(dict(offers=offers))


@route("/j/email/affiliate_email")
class ActiveAffiliateEmail(JsonLoginView):

    def get(self):
        offer_ids = self.get_arguments('offer_ids[]')
        active_offer_affiliate = OfferAffiliate._query(offer_ids=offer_ids)

        affiliate_emails = []
        for off_aff in active_offer_affiliate:
            aff_id = off_aff.affiliate_id
            if aff_id:
                aff = User.find_one(dict(_id=int(aff_id)))
                if aff:
                    affiliate_emails.append(','.join(aff.email))

        self.finish(dict(affiliate_emails=affiliate_emails))