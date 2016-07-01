#!/usr/bin/env python3

import requests
import getopt, sys
import configer
import threading

class Downloader(object):

    # Init the Downloader
    def __init__(self, configer):
        self.configer = configer
        self.file_lock = threading.Lock()
        self.block_size = 1000
        self.thread_list = list()

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
                with self.file_lock:
                    with open(
                        self.configer.path, 'r+b',
                        buffering = 1
                    ) as f:
                        f.seek(start_point)
                        f.write(bunch)
                        f.flush()
                start_point += self.block_size

    # start and mornit
    def start_download(self):
        t = threading.Thread(target=self._download)
        t.start()

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
