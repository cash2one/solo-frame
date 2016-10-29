# coding=utf-8
import os
from gearman import GearmanClient
import json


class EmailClient(object):
    '''邮件发送gearman客户端'''

    def __init__(self, hosts):
        self.client = GearmanClient(hosts)

    def create_message(self, subject, text=None, attachment_path=None, html_path=None):
        '''
        :param msg_content: 消息内容
        :param image_path: 图片路径
        :param attachment_path: 附件路径
        :param html_path: 模板路径
        :return:
        '''
        msg = {'subject': subject, 'text': text}

        if attachment_path:
            with open(attachment_path, 'rb') as fb:
                attachment_file = fb.read()
                msg['attachment_name'] = os.path.basename(attachment_path)
                msg['attachment'] = attachment_file.encode('base64')

        if html_path:
            with open(html_path, 'rb') as fb:
                html_file = fb.read()
                msg['html'] = html_file

        return msg

    def send(self, email_server, email_server_port, sender, receiver, use_name, pass_word, worker, msg, _id):

        task_job_list = []
        for r in receiver:
            content = dict(
                username=use_name,
                password=pass_word,
                email_server=email_server,
                email_server_port=email_server_port,
                sender=sender,
                receiver=r,
                msg=msg,
                email_id=_id
            )
            task_job_list.append(dict(task=worker, data=json.dumps(content)))
        res = self.client.submit_multiple_jobs(task_job_list, background=True, wait_until_complete=False)
        return res

    def check_email_status(self, res):
        retried_connection_failed_requests = self.client.submit_multiple_requests(res, wait_until_complete=True, poll_timeout=1.0)
        for r in retried_connection_failed_requests:
            print r


if __name__ == '__main__':
    pass
