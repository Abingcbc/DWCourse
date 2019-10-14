# -*- coding: utf-8 -*-

from scrapy import signals
import random
import time
import requests
from amazon_movies.utils import *
import traceback

class AmazonMoviesDownloaderMiddleware(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        new_request(request)
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            if response.status == 404:
                with open("404.log", "a") as file:
                    file.write(response.url + "\n")
                    return response
            log('ErrorCode: ' + str(response.status) + ' ' + str(response.url))
            # requests.get('http://127.0.0.1:5000/delete?proxy=' + 
            # request.meta['proxy'].replace('http://',''))
            return new_request(request)
        return response

    def process_exception(self, request, exception, spider):
        log('MyError: ')
        log(traceback.format_exc())
        # requests.get('http://127.0.0.1:5010/delete?proxy='+
        # request.meta['proxy'].replace('http://',''))
        with open('error.log', 'a') as file:
            file.write(request.url.split('/')[-1] + '\n')
            file.write(traceback.format_exc())