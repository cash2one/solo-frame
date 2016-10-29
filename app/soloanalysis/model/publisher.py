# coding:utf-8
from solo.web.mongo import Doc
from app.web.model.gid import gid as _gid


class Publisher(Doc):
    structure = dict(
        _id=int,
        publisher_id=int,
        name=str,
        slot=list,
    )


if __name__ == '__main__':
    publisher = Publisher(
        dict(
            _id=_gid('analysis'),
            publisher_id=4,
            name='jay',
            slot=[13,14,15,16]
        )
    )
    publisher.save()