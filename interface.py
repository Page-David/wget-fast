#!/usr/bin/env python3

# Module for output text config and speed output.

class Version_Info(object):
    
    def __init__(self):
        self.name = "Wget-Fast"
        self.version = "0.90"
        self.author = "by Page David"
        self.email = "email to David991010@gmail.com"

    def out(self):
        print('{} {}'.format(self.name, self.version))

    def out_detail(self):
        print('{} {}'.format(self.author, self.email))

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

class Error_List(object):

    def __init__(self):
        self.Errors = {'nothing_input': "No URL input, exiting.."}

    def out(self, error):
        print(self.Errors[error])

