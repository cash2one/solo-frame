#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import LoginView, JsonLoginView
from app.new_pingstart.model.network import NetWork as NWork
from app.new_pingstart.model.slots import Slots, TYPE_MAP
from solo.lib.jsob import JsOb


@route("/network")
class NetWork(LoginView):

    def get(self):
        user_id = self.current_user_id
        networks = NWork.find(dict(user_id={"$in": [int(user_id), None]}, deleted=False))
        for n in networks:
            spec = dict(
                appId=int(user_id),
                network={
                    '$elemMatch': dict(network_id=int(n._id))
                },
                deleted=False,
            )
            slots = Slots.find(spec)
            n['ads'] = []
            for s in slots:
                ad = {}
                ad['units'] = s.name
                ad['format'] = TYPE_MAP.get(s.slotType)
                ad['slot_id'] = s._id
                for bind_network in s.network:
                    if bind_network.get('network_id') == int(n._id):
                        ad['placement'] = bind_network.get('placement_id')
                n['ads'].append(ad)
            n['ad_count'] = len(n['ads'])
        self.render(networks=networks)


@route("/network/create")
class NetWork(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        content = self.json
        name = content.name
        if NWork.count(dict(name=name, user_id=int(user_id))):
            err.name = u'This NetWork Name has been used!'

        if not err:
            adapter = content.adapter
            auth_manager = content.auth_manager
            sdk = content.sdk
            NWork.create(user_id=user_id, name=name, adapter=adapter, auth_manager=auth_manager, sdk=sdk)

        self.render(err)


@route('/network/update')
class NetWork(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        content = self.json
        network_id = content._id
        network = NWork.find_one(dict(_id=int(network_id)))
        name = content.name
        if name != network.name and NWork.count(dict(name=name, user_id=int(user_id))):
            err.name = u'This name has been used!'

        if not err:
            network.name = name
            network.auth_manager = content.auth_manager
            network.save()

            spec = dict(
                network={
                    '$elemMatch': dict(network_id=int(network._id))
                },
                deleted=False,
            )
            slots = Slots.find(spec)
            for s in slots:
                for n in s.network:
                    if n.get('network_id') == int(network._id):
                        n['network_name'] = name
                s._id = int(s._id)
                s.save()

        self.render(err)




