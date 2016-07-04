#!/usr/bin/env python3

import requests
import getopt, sys
import configer
import threading
import time
import queue

class Downloader(object):

    # Init the Downloader
    def __init__(self, configer):
        self.configer = configer
        self.file_lock = threading.Lock()
        self.block_size = 1000
        self.thread_list = list()
        self.speed = dict() # Download Speed for each thread
        self.worker_com = queue.Queue() # queue for works send speed info
        self.total_speed = 0 # sum of the speed
        self.num_speed = [0] # the speed when how many threads are started
                             # 0 thread meands speed is 0
        self.worker_count = 0

    # Setup the slaver
    def _download(self):
        # Start download partital content when queue not empty
        while not self.configer.down_queue.empty():
            data_range = self.configer.down_queue.get()
            headers = {
                'Range': 'bytes={}-{}'.format(*data_range)
            }
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
                        f.write(bunch)
                        f.flush()
                start_point += self.block_size
                self.worker_com.put((
                    threading.current_thread().name,
                    int(self.block_size / (time.time() - _time))
                ))
            self.configer.down_queue.task_done()

    # speed monitor
    def speed_monitor(self):
        while len(self.thread_list)>0:
            try:
                info = self.worker_com.get_nowait()
                self.speed[info[0]] = info[1]
            except queue.Empty:
                time.sleep(0.1)
                continue
            sys.stdout.write('\b'*64 + '{:10}'.format(self.total_speed)
                + '  thread num ' + '{:2}'.format(self.worker_count))
            sys.stdout.flush()

    # start and mornit
    def start_download(self):
        t = threading.Thread(target = self._download)
        self.thread_list.append(t)
        t.start()
        monitor = threading.Thread(target = self.speed_monitor)
        monitor.start()
        while self.thread_list:
            self.total_speed = sum(list(self.speed.values()))
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


def main():
    # Try to get options by user
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:')
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o =='-s':
            saveto = a
    download_configer = configer.Download_Configer(args[0], saveto)
    # Fire...
    downloader = Downloader(download_configer)
    downloader.start_download()
        
if __name__ == '__main__':
    main()
