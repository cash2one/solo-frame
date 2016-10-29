#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from _base import LoginView, JsonLoginView, JsonErrView
from app.new_pingstart.model.network import NetWork
from app.new_pingstart.model.slots import Slots, TYPE_MAP
from solo.lib.jsob import JsOb
from app.new_pingstart.controller.tools import DateTime
from datetime import datetime

@route("/slot")
class Slot(LoginView):

    def get(self):
        self.render()


@route("/slots")
class Slot(JsonLoginView):

    def get(self):
        user_id = self.current_user_id
        page = int(self.get_argument('page', 1))
        limit = int(self.get_argument('limit', 0))
        name = self.get_argument('name', '')
        offset = limit * (page - 1)
        slots, slots_count = Slots.get_list(user_id, keyword=name, limit=limit, offset=offset)
        for slot in slots:
            slot['slot_type'] = TYPE_MAP.get(slot.slotType, '')
        self.finish(dict(slots=slots if slots else [], slots_count=slots_count))


@route("/slot/create")
class Slot(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        content = self.json
        if not content.slotType:
            err.slotType = u'SlotType can\'t be empty!'
        if not content.name:
            err.name = u'Slot Name can\'t be empty!'
        elif Slots.count(dict(name=content.name, appId=int(user_id))):
            err.name = u'The slot name {} has been used!'.format(content.name)

        if not err:
            user_id = self.current_user_id
            slot = Slots.edit(user_id, None, content.slotType, content.name)
            ps_network = NetWork.pingstart(user_id)
            adapter = ps_network.adapter_model.get(TYPE_MAP.get(content.slotType))
            network = [
                dict(
                    network_id=ps_network._id,
                    network_name=ps_network.name,
                    is_auth=True,
                    placement_id='publisher_id={user_id};slot_id={slot_id}'.format(user_id=user_id, slot_id=slot._id),
                    is_paused=False,
                    adapter=adapter,
                    priority=0
                )
            ]
            slot.network = network
            slot.save()

        self.render(err)


@route("/slot/edit/(\d+)")
class SlotEdit(LoginView):

    def get(self, slot_id):
        user_id = self.current_user_id
        slot = Slots.find_one(dict(_id=int(slot_id)))
        slot_type = TYPE_MAP.get(slot.slotType)
        networks = NetWork.find(dict(user_id={"$in": [int(user_id), None]}, deleted=False, name={"$ne": 'PingStart'}))
        networks = [net for net in networks if net.adapter_model.get(slot_type)]
        slot['network_select'] = networks
        slot['bind_networks'] = slot.network
        slot['slot_type'] = TYPE_MAP.get(slot.slotType, '')
        slot['model'] = slot.model
        slot['appBlackList'] = '\n'.join(slot.appBlackList) if slot.appBlackList else ''
        self.render(slot=slot)


@route("/slot/update")
class SlotEdit(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        content = self.json
        slot_id = content.slot_id
        slot_name = content.slot_name
        network = content.network
        app_black_list = content.appBlackList
        model = content.model
        slot = Slots.find_one(dict(_id=int(slot_id)))
        if slot_name != slot.name and Slots.count(dict(name=slot_name, appId=int(user_id), deleted=False)):
            err.name = u'This Slot Name has been used!'

        if not err:
            slot.name = slot_name
            for n in network:
                net_id = n.get('network_id')
                net = NetWork.find_one(dict(_id=int(net_id)))
                if n.get('auth_manager'):
                    auth_manager = n.pop('auth_manager')
                    net.auth_manager = auth_manager
                    net.save()
                n['network_id'] = int(n['network_id'])
                n['adapter'] = net.adapter_model.get(TYPE_MAP.get(slot.slotType))
            slot.network = network
            slot.model = model
            slot.appBlackList = app_black_list.split('\n')
            slot.last_operated = DateTime().today
            slot.save()

        self.render(err)


@route("/slot/delete/(\d+)")
class Slot(JsonLoginView):

    def post(self, slot_id):
        slot = Slots.find_one(dict(_id=int(slot_id)))
        slot.deleted = True
        slot.save()
        self.finish()


@route("/slot/search")
class Slot(JsonLoginView):

    def post(self):
        user_id = self.current_user_id
        search_query = self.json.search_query
        name = search_query.get('name', None)
        limit = search_query.get('limit', 0)
        page = search_query.get('page', 1)
        offset = int(limit) * (int(page)-1) if limit and page else 0
        slots, slots_count = Slots.get_list(user_id, keyword=name, limit=limit, offset=offset)
        for slot in slots:
            slot['slot_type'] = TYPE_MAP.get(slot.slotType, '')
        self.finish(dict(slots=slots if slots else [], slots_count=slots_count))


@route("/slot/network/auth")
class Slot(JsonLoginView):

    def post(self):
        content = self.json
        network_id = content.network_id
        network = NetWork.find_one(dict(_id=int(network_id)))
        network.auth_manager = content.auth_manager
        network.save()
        self.finish(dict(network=network))


@route("/slot/networks")
class Slot(JsonErrView):

    def get(self):
        err = JsOb()
        publisher_id = self.get_argument('publisher_id', None)
        if not publisher_id:
            err.publisher_id = u'Publisher_id can\'t be None'

        slot_id = self.get_argument('slot_id', None)
        if not slot_id:
            err.slot_id = u'Slot_id can\'t be None'
        else:
            slot = Slots.find_one(dict(_id=int(slot_id), appId=int(publisher_id)))
            if not slot:
                err.slot = u'The slot is not exist!'
            elif not slot.network:
                err.network = u'The slot have not bind any network!'

        if not err:
            res = dict(ad=[])
            network_weights = slot.network[::-1]
            for net in slot.network:
                if not net.get('is_paused'):
                    placement_id_dict = dict()
                    placement_ids = net.get('placement_id').split(";")
                    p_id_list = [p_id.split('=') for p_id in placement_ids if p_id]
                    for p_id in p_id_list:
                        placement_id_dict[p_id[0]] = p_id[1]

                    ad_unit_id = placement_id_dict.get('ad_unit_id')
                    if ad_unit_id and ad_unit_id[0] == u'[':
                        ad_unit_id = ad_unit_id[1:-1].split(',')
                        placement_id_dict['ad_unit_id'] = ad_unit_id

                    net_new = dict(
                        weight=network_weights.index(net),
                        platfrom=net.get('network_name'),
                        custom_cls=net.get('adapter'),
                        placement_id=placement_id_dict,
                    )
                    res['ad'].append(net_new)

            self.finish(res)
        else:
            self.render(err)


@route("/placement_id/verify")
class VPlacement(JsonLoginView):

    def post(self):
        err = JsOb()
        user_id = self.current_user_id
        placement_id = self.json.placement_id
        network_id = self.json.network_id
        spec = dict(
            appId=int(user_id),
            network={
                '$elemMatch': dict(placement_id=placement_id, network_id=int(network_id))
            },
            deleted=False,
        )
        slot = Slots.find_one(spec)
        if slot:
            err.placement = u'The placement_id has been used!'

        self.render(err)


@route("/slot/status")
class Status(JsonLoginView):

    def post(self):
        content = self.json
        slot_id = content.slot_id
        slot = Slots.find_one(dict(_id=int(slot_id)))
        if slot.status == 1:
            slot.status = 0
        else:
            slot.status = 1
        slot.last_operated = datetime.now().strftime('%Y-%m-%d')
        slot.save()