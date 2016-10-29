# coding=utf-8
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey

class EModelNotFound(BaseException):
    pass


class EmailModel(Doc):

    structure = dict(
        _id=int,
        model_name=str,
        content=str,
        createdTime=str,
        last_update=str,
        deleted=bool
    )

    _t = DateTime()

    indexes = [
        {'fields': ['_id']},
        {'fields': ['model_name', 'deleted']},
    ]

    default_values = {
        'createdTime': _t.current_time,
        'last_update': _t.current_time,
        'deleted': False
    }

    @classmethod
    def _create(cls, **kwargs):
        e_model = EmailModel(dict(
            _id=_gid(GidKey.e_model_key),
            model_name=kwargs.get('model_name'),
            content=kwargs.get('content')
        ), True)
        e_model.save()

    @classmethod
    def _delete(cls, _id):
        e_model = cls._get(_id)
        e_model.deleted = True
        e_model.save()
        return True

    @classmethod
    def _get(cls, _id, fields=None):
        if not _id:
            return {}
        spec = dict(_id=int(_id))
        if not fields:
            e_model = cls.find_one(spec)
        else:
            e_model = cls.find_one(spec, fields)
        return e_model

    @classmethod
    def _query(cls, spec, fields=None):
        return cls.find_one(spec)

    @classmethod
    def _update(cls, _id, model_name, content):
        e_model = cls._get(_id)
        e_model._id = int(_id)
        e_model.model_name = model_name if model_name else e_model.model_name
        e_model.content = content if content else e_model.content
        e_model.last_update = cls._t.current_time
        e_model.save()


if __name__ == '__main__':
    kwargs = {'content': 'demo'}
    e = EmailModel()
    e._create(**kwargs)
    # EmailModel.find({}, {'_id': 1, 'model_name': 1})