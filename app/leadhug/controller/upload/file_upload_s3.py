#!/usr/bin/env python
# coding=utf-8
from __future__ import division
import tornado
import _env  # noqa
import math
import os
from filechunkio import FileChunkIO
import threading
import Queue
from app.leadhug.controller.upload import StorageS3


class UploadS3(StorageS3):

    def __init__(self,  file_path, key_name):
        super(UploadS3, self).__init__()
        self.file_path = file_path
        self.key_name = key_name
        self.thread_count = 10
        self.chunk_size = 8 << 20

    class Chunk:

        def __init__(self, num, offset, length):
            self.num = num
            self.offset = offset
            self.length = length

    def queue_init(self, file_size):
        chunk_count = int(math.ceil(file_size*1.0/self.chunk_size))
        _queue = Queue.Queue(maxsize=chunk_count)
        for i in range(0, chunk_count):
            offset = self.chunk_size * i
            length = min(self.chunk_size, file_size-offset)
            chunk = self.Chunk(i+1, offset, length)
            _queue.put(chunk)
        return _queue

    def upload_chunk(self, bucket_mp, _queue, headers, _type):
        ''' upload file chunk '''
        while not _queue.empty():
            chunk = _queue.get()
            fp = FileChunkIO(self.file_path, 'r', offset=chunk.offset, bytes=chunk.length)
            if _type == 'big':
                bucket_mp.upload_part_from_file(fp, part_num=chunk.num, headers=headers)
            else:
                bucket_mp.set_contents_from_file(fp, headers=headers, policy='public-read')
            fp.close()
            _queue.task_done()

    def upload_file(self, _queue, headers, _type):
        ''' upload file '''
        if _type == 'big':
            bucket_mp = self.get_bucket().initiate_multipart_upload(self.key_name, policy='public-read')
        else:
            bucket_mp = self.get_bucket().new_key(self.key_name)

        if _queue.qsize() < self.thread_count:
            self.thread_count = _queue.qsize()

        for i in range(0, self.thread_count):
            t = threading.Thread(target=self.upload_chunk, args=(bucket_mp, _queue, headers, _type))
            t.setDaemon(True)
            t.start()
        _queue.join()
        if _type == 'big':
            bucket_mp.complete_upload()
        return bucket_mp

    @tornado.gen.coroutine
    def upload_start(self, content_type='application/octet-stream'):
        file_size = os.stat(self.file_path).st_size
        _queue = self.queue_init(file_size)
        headers = {
            "Content-Type": content_type
        }
        _type = 'big' if file_size >= 5242880 else 'small'
        res = yield self.upload_file(_queue, headers, _type)
        raise tornado.gen.Return(res)


if __name__ == '__main__':
    import time
    s = time.time()
    u = UploadS3('/home/lipf/Documents/report.csv', 'test')
    res = u.upload_start()
    e = time.time()
    print (e - s)
    print 'done, res=', type(res)
    print res.done()