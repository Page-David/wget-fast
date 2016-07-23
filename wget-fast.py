#!/usr/bin/env python3

import getopt, sys, os
import configer
import HTTP_Downloader
import interface

def main():
    # Print Version info
    info = interface.Version_Info()
    info.out()
    # Init Error List on input
    input_errors = interface.Error_List()
    # Try to get options by user
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:v')
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o == '-v':
            info.out_detail()
            sys.exit(1)
        elif o =='-s':
            saveto = a[0].replace('~', os.path.expanduser('~')) + a[1:]
    # No URL input
    if not args:
        input_errors.out('nothing_input')
        sys.exit(2)
    if not 'saveto' in locals():
        saveto = os.getcwd()
    download_configer = configer.Download_Configer(args[0], saveto)
    # Fire...
    if download_configer.protocol.lower() in ('http', 'https'):
        downloader = HTTP_Downloader.Downloader(download_configer)
        downloader.start_download()
        
if __name__ == '__main__':
    main()
