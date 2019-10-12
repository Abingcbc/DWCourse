# -*- coding: utf-8 -*-

import random
import time
import requests
from amazon_movies.utils import *

class AmazonMoviesDownloaderMiddleware(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_request(self, request, spider):
        request = new_request(request)

    def process_response(self, request, response, spider):
        if response.status != 200:
            if response.status == 404:
                with open("404.log", "a") as file:
                    file.write(response.url + "\n")
                    return response
            log('ErrorCode: ' + str(response.status))
            requests.get('http://127.0.0.1:5000/delete/' + 
            request.meta['proxy'].replace('http://',''))
            return new_request(request)
        return response

    def process_exception(self, request, exception, spider):
        log('MyError: '+str(exception) + '\n')
        requests.get('http://127.0.0.1:5000/delete/'+
        request.meta['proxy'].replace('http://',''))
        with open('error.log', 'a') as file:
            file.write(request.url.split('/')[-1] + '\n')
            file.write('Retry times overflow\n')