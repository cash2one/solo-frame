# coding:utf-8
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid
from yajl import loads, dumps


class Activity(Doc):
    structure = dict(
        _id=int,
        publisher_id=int,
        slot_id=int,
        country=str,
        time=str,
        new=int,
        active=int,
        total=int,
    )

    @classmethod
    def aggregate(cls, *args, **kwds):
        return cls._collection.aggregate(*args, **kwds)

    @classmethod
    def time_country(cls, self):
        spec = loads(self.request.body)
        if spec['time']:
            spec['time'] = {'$gte': spec['time']['start'], '$lte': spec['time']['end']}
        for k,v in spec.items():
            if not v:
                del spec[k]
        sort_by_time = Activity.aggregate([
            {'$match': spec},
            {'$group': {'_id': '$time', 'new': {'$sum': '$new'}, 'active': {'$sum': '$active'},'total': {'$sum': '$total'}}},
            {'$sort': {'_id': -1}}
        ])
        sort_by_time = sort_by_time['result']
        sort_by_time = {'count': len(sort_by_time),'sort_by_time':sort_by_time}
        sort_by_country = Activity.aggregate([
            {'$match': spec},
            {'$group': {'_id': '$country', 'new': {'$sum': '$new'}, 'active': {'$sum': '$active'},'total': {'$sum': '$total'}}},
            {'$sort': {'_id': 1}}
        ])
        sort_by_country = sort_by_country['result']
        sort_by_country = {'count': len(sort_by_country),'sort_by_country':sort_by_country}
        return sort_by_time, sort_by_country

    @classmethod
    def export_time_country(cls, self):
        spec = loads(self.get_argument('filter'))

        if spec['time']:
            spec['time'] = {'$gte': spec['time']['start'], '$lte': spec['time']['end']}
        for k,v in spec.items():
            if not v:
                del spec[k]
        # ac = Activity.find(spec)
        sort_by_time = Activity.aggregate([
            {'$match': spec},
            {'$group': {'_id': '$time', 'new': {'$sum': '$new'}, 'active': {'$sum': '$active'},'total': {'$sum': '$total'}}},
            {'$sort': {'_id': 1}}
        ])
        sort_by_time = sort_by_time['result']
        sort_by_country = Activity.aggregate([
            {'$match': spec},
            {'$group': {'_id': '$country', 'new': {'$sum': '$new'}, 'active': {'$sum': '$active'},'total': {'$sum': '$total'}}},
            {'$sort': {'_id': 1}}
        ])
        sort_by_country = sort_by_country['result']
        return sort_by_time, sort_by_country

    @classmethod
    def get_chart(cls, self):
        spec = loads(self.request.body)
        if spec['time']:
            spec['time'] = {'$gte': spec['time']['start'], '$lte': spec['time']['end']}
        for k,v in spec.items():
            if not v:
                del spec[k]
        value = Activity.aggregate([
            {'$match': spec},
            {'$group': {'_id': '$time', 'new': {'$sum': '$new'}, 'active': {'$sum': '$active'},'total': {'$sum': '$total'}}},
            {'$sort': {'_id': 1}}
        ])

        new = []
        active = []
        total = []
        x = []
        for item in value['result']:
            x.append(item['_id'])
            new.append(item['new'])
            active.append((item['active']))
            total.append((item['total']))
        result = {
            'new_data': {
                'x': x,
                'y': new
            },
            'active_data': {
                'x': x,
                'y': active
            },
            'total_data': {
                'x': x,
                'y': total
            }
        }
        return result
if __name__ == "__main__":
    activity = Activity(
        dict(
            _id=_gid('activity'),
            publisher_id=1,
            slot_id=2,
            country='en',
            time='2016-04-18',
            new=50,
            active=51,
            total=52,
        )
    )
    activity.save()
