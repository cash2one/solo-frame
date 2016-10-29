# coding=utf-8
from solo.web.mongo import Doc
from app.leadhug.controller.tools import DateTime
from app.web.model.gid import gid as _gid
from app.leadhug.model import GidKey
from app.leadhug.controller.gearman_package.email_client import EmailClient
from solo.config import GEARMAN_SERVER
from solo.config import GEARMAN_CLIENT as e_conf


class EMail(Doc):
    structure = dict(
        _id=int,
        user_id=int,
        model_id=int,
        subject=str,
        sender=str,
        receiver=list,
        fail_receiver=[
            {
                'receiver': str,
                'reason': str,
            }
        ],
        message=str,
        createdTime=str,
        sendTime=str,
    )

    _t = DateTime()

    indexes = [
        {'fields': ['_id']},
        {'fields': ['receiver']},
    ]

    default_values = {
        'sender': e_conf.get('sender'),
        'fail_receiver': [],
        'createdTime': _t.current_time,
        'sendTime': _t.current_time
    }

    gearman_email_job = EmailClient(GEARMAN_SERVER)

    @classmethod
    def _create(cls, **kwargs):
        e_mail = EMail(gen_skel=True)
        e_mail._id = _gid(GidKey.email_key)
        e_mail.user_id = int(kwargs.get('user_id'))
        e_mail.model_id = int(kwargs.get('model_id'))
        e_mail.subject = kwargs.get('subject')
        e_mail.sender = kwargs.get('sender', e_mail.sender)
        e_mail.receiver = kwargs.get('receiver')
        e_mail.message = kwargs.get('message')
        e_mail.save()
        cls._send(e_mail)  # 此处暂时先存后发送

    @classmethod
    def _send(cls, e_mail):
        message = cls.gearman_email_job.create_message(e_mail.subject, e_mail.message)
        res = cls.gearman_email_job.send(
            e_conf.get('email_server'),
            e_conf.get('email_server_port'),
            e_mail.sender,
            e_mail.receiver,
            e_conf.get('user_name'),
            e_conf.get('password'),
            e_conf.get('worker'),
            message,
            e_mail._id,
        )
        return res

    @classmethod
    def _check_email_stats(cls, _id, res):
        cls.gearman_email_job.check_email_status(res)

    @classmethod
    def _query(cls, user_id, limit=0, offset=0):
        spec = dict(user_id=int(user_id))
        fields = dict(_id=1, subject=1, sendTime=1)
        return cls.find(spec, fields, limit=limit, skip=offset)

    @classmethod
    def _fail_email(cls, _id, receiver, reason=None):
        e = cls.find_one({'_id': int(_id)})
        e.fail_receiver.append(dict(receiver=receiver, reason=reason))
        e.save()


if __name__ == '__main__':
    EMail._send(32)
    print 'aaaa'
    pass
