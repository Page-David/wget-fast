#!/usr/bin/env python3

# Module for output text config and speed output.

def info_out(key, *values):

    info_dict = {
            'HTTP_REQUEST': 'Sending HTTP request to server...',
            'PARTITAL_SUPPORT': 'The server suport multithread download.',
            'PARTITAL_NOT_SUPPORT': 'The server do not support partital'
            'content, please do not terminate the download.',
            'CONNECTION_ERROR': 'We get a connection error, try again'
            'later.{}',
            'CONTENT_LENGTH': 'Total content length:{}Bytes'
        }
    print(info_dict.get(key, 'WARM: Your interface module may be broken,'
            'please send issue to github repository').format(*values))

