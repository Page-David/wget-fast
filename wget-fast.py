#!/usr/bin/env python3

import getopt, sys
import configer
import HTTP_Downloader

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
    downloader = HTTP_Downloader.Downloader(download_configer)
    downloader.start_download()
        
if __name__ == '__main__':
    main()
