# coding=utf-8
from __future__ import division
from pymongo import Connection


class Data(object):

    def __init__(self, old_db_host, new_db_host, insert_number):
        self.old_db = Connection(old_db_host).pingstart
        self.new_db = Connection(new_db_host).new_pingstart
        self.insert_number = int(insert_number)

    def country_data(self):
        old_coll = self.old_db.slot_cmapaign_detail
        new_coll = self.new_db.countryReport

        old_data = old_coll.find()
        insert_data_list = []
        i = 0
        for doc in old_data:
            i += 1
            createdTime = doc.get('createdTime')
            slot_id = doc.get('slotId')
            country_datas = doc.get('country')
            for c, d in country_datas.items():
                country_data_dict = dict()
                country_data_dict['createdTime'] = createdTime
                country_data_dict['slot_id'] = slot_id
                country_data_dict['country'] = c
                country_data_dict['impression'] = d.get('impression', '')
                country_data_dict['conversion'] = d.get('conversion', '')
                country_data_dict['show_conversion'] = d.get('show_conversion', '')
                country_data_dict['revenue'] = d.get('income', '')
                country_data_dict['show_revenue'] = d.get('show_income', '')
                country_data_dict['request'] = d.get('request', '')
                country_data_dict['click'] = d.get('click', '')
                country_data_dict['show_click'] = d.get('show_click', '')
                country_data_dict['network'] = 'PingStart'
                insert_data_list.append(country_data_dict)

            if i % self.insert_number == 0:
                new_coll.insert(insert_data_list)
                insert_data_list = []

        if insert_data_list:
            new_coll.insert(insert_data_list)


if __name__ == '__main__':
    database = Data('mongo','mongo', 1000)
    database.country_data()
