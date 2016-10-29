#!/usr/bin/env python
# coding=utf-8
from tornado.ioloop import IOLoop
from pymongo import MongoClient
import _env  # noqa
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from solo.config import MONGO_CONFIG, DBNAME


class ScheInterface(object):

    def __init__(self, job_type, store_executor_alias, process_count):
        self.sche = TornadoScheduler()
        self.host = MONGO_CONFIG.get('host')
        self.mongo_client = MongoClient(self.host)
        self.job_type = job_type
        self.mongo_job_store = MongoDBJobStore(collection='job', database=DBNAME, client=self.mongo_client)
        self.store_executor_alise = store_executor_alias
        self.process_poll = ProcessPoolExecutor(process_count)

    def add_date_job(self, func, args, run_date, max_instances, listener_fun):
        self.sche.add_jobstore(self.mongo_job_store, alias=self.store_executor_alise)
        self.sche.add_executor(self.process_poll, alias=self.store_executor_alise)
        self.sche.add_listener(listener_fun, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
        try:
            self.sche.add_job(func, self.job_type, args=args, run_date=run_date, max_instances=max_instances, jobstore=self.store_executor_alise)
            return True
        except Exception:
            return False


def func(timestamp):
    print timestamp


if __name__ == '__main__':
    sche_interface = ScheInterface('date', 'offer', 5)
    date = '2016-05-27 09:58:00'
    # sche_interface.add_date_job(func, [date], date, 5)
    # sche_interface.sche.start()
    print 'start....'
    IOLoop.instance().start()








