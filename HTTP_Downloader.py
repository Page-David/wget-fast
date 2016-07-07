#!/usr/bin/env python3

import requests
import threading
import time
import queue
import requests
import sys
import humanfriendly
import Monitor

class Downloader(object):

    # Init the Downloader
    def __init__(self, configer):
        self.configer = configer
        self.file_lock = threading.Lock()
        self.block_size = 1000
        self.thread_list = list()
        self.status = dict() # Status for each thread
        self.start_time = dict()
        self.downloaded = dict()
        self.worker_com = queue.Queue() # queue for works send speed info
        self.total_speed = 0 # sum of the speed
        self.num_speed = [0] # the speed when how many threads are started
                             # 0 thread meands speed is 0
        self.worker_count = 0
        self.monitor = None

    # Setup the slaver
    def _download(self):
        # Start download partital content when queue not empty
        while not self.configer.down_queue.empty():
            data_range = self.configer.down_queue.get()
            headers = {
                'Range': 'bytes={}-{}'.format(*data_range)
            }
            self.start_time[threading.current_thread().name]\
                = time.time()
            self.downloaded[threading.current_thread().name] = 0
            response = requests.get(
                self.configer.url, stream = True,
                headers = headers
            )
            start_point = data_range[0]
            for bunch in response.iter_content(self.block_size):
                _time = time.time()
                with self.file_lock:
                    with open(
                        self.configer.path, 'r+b',
                        buffering = 1
                    ) as f:
                        f.seek(start_point)
                        self.downloaded[threading.current_thread().name] += f.write(bunch)
                        f.flush()
                start_point += self.block_size
                self.status[threading.current_thread().name]\
                        = humanfriendly.format_size(
                            int(self.downloaded[threading.current_thread().name]\
                                    /(time.time()\
                                    - self.start_time[threading.current_thread().name]))
                        ) + '/s'
            self.configer.down_queue.task_done()
        self.status[threading.current_thread().name] = 'Done'

    # speed monitor
    def speed_monitor(self):
        self.monitor = Monitor.Speed_Monitor()
        while len(self.thread_list) > 0:
            time.sleep(.5)
            self.monitor.refresh_monitor(self.status)
        self.monitor.finish_monitor()


    # start and mornit
    def start_download(self):
        t = threading.Thread(target = self._download)
        self.thread_list.append(t)
        t.start()
        monitor = threading.Thread(target = self.speed_monitor,
            name = 'monitor')
        monitor.start()
        while self.thread_list:
            self.total_speed = \
                    sum([i for i in list(self.status.values()) if type(i) == int])###need modify#####
            self.worker_count = len(self.thread_list)
            self.thread_list[:] = [t for t in self.thread_list 
                    if t.isAlive()]
            self.num_speed[self.worker_count - 1] = self.total_speed
            if (self.num_speed[self.worker_count - 1] >= self.num_speed[self.worker_count - 2]
                    and self.worker_count <= self.configer.max_thread 
                    and not self.configer.down_queue.empty()):
                t = threading.Thread(target = self._download)
                self.thread_list.append(t)
                t.start()
                self.num_speed.append(0)
        print('')
