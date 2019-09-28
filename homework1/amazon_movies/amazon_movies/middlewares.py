# -*- coding: utf-8 -*-

from scrapy import signals
import random
import time
import requests

class AmazonMoviesSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonMoviesDownloaderMiddleware(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
        ]

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        request.meta['proxy'] = self.proxy()
        print('\nUsing proxy: ' + request.meta['proxy']+'\n')

    def proxy(self):
        proxy = eval(requests.get("http://127.0.0.1:5010/get/").text)['proxy']
        return 'http://' + proxy

    def process_response(self, request, response, spider):
        if response.status != 200 or response.body is None:
            self.delete_proxy(request.meta['proxy'].replace('http://',''))
            request.meta['proxy'] = self.proxy()
            request.headers['User-Agent'] = random.choice(self.user_agents)
            return request
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' in request.meta.keys():
            self.delete_proxy(request.meta['proxy'].replace('http://',''))
        request.meta['proxy'] = self.proxy()
        request.headers['User-Agent'] = random.choice(self.user_agents)
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
    
    def delete_proxy(self, proxy):
        print('\nProxy invalid: ' + proxy + '\n')
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
