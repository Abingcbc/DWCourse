# -*- coding: utf-8 -*-

import random
import time
import requests
import amazon_movies.utils as utils

class AmazonMoviesDownloaderMiddleware(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_request(self, request, spider):
        request = utils.new_request(request)
        print('Using proxy: ' + request.meta['proxy'])
        print(request.url + '\n')
        print(request.meta['proxy'])

    def process_response(self, request, response, spider):
        if response.status != 200 or response.body is None:
            print('ErrorCode: ' + str(response.status))
            utils.delete_proxy(request.meta['proxy'].replace('http://',''))
            return utils.new_request(request)
        return response

    def process_exception(self, request, exception, spider):
        print('MyError: '+str(exception) + '\n')
        utils.delete_proxy(request.meta['proxy'].replace('http://',''))
        if 'retry_times' not in request.meta.keys():
            request.meta['retry_times'] = 0
        if request.meta['retry_times'] >= 100:
            with open('error.log', 'a') as file:
                file.write(request.url.split('/')[-1] + '\n')
                file.write('Retry times overflow\n')
        else:
            return utils.new_request(request)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
