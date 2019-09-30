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
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def init_request(self, request):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        request.meta['proxy'] = self.proxy()
        if 'retry_times' in request.meta.keys():
            request.meta['retry_times'] += 1
        else:
            request.meta['retry_times'] = 0
        return request

    def process_request(self, request, spider):
        request = self.init_request(request)
        print('Using proxy: ' + request.meta['proxy'])
        print(request.url + '\n')

    def proxy(self):
        r = eval(requests.get("http://127.0.0.1:5010/get/").text)
        while 'proxy' not in r:
            r = eval(requests.get("http://127.0.0.1:5010/get/").text)
        proxy = r['proxy']
        return "http://" + proxy

    def process_response(self, request, response, spider):
        if response.status != 200 or response.body is None:
            print('ErrorCode: ' + str(response.status) + '\n')
            self.delete_proxy(request.meta['proxy'].replace('http://',''))
            return self.init_request(request)
        return response

    def process_exception(self, request, exception, spider):
        print('Error: '+str(exception) + '\n')
        if 'retry_times' not in request.meta.keys():
            request.meta['retry_times'] = 0
        if request.meta['retry_times'] >= 100:
            with open('error.log', 'a') as file:
                file.write(request.url.split('/')[-1] + '\n')
                file.write('Retry times overflow\n')
        else:
            return self.init_request(request)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
    
    def delete_proxy(self, proxy):
        print('Proxy invalid: ' + proxy + '\n')
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
