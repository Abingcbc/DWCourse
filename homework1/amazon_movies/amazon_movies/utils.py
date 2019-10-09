import requests
import random

user_agents = [
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

def proxy():
    r = eval(requests.get("http://127.0.0.1:5010/get/").text)
    # wait until there is available proxy
    while 'proxy' not in r:
        r = eval(requests.get("http://127.0.0.1:5010/get/").text)
    proxy = r['proxy']
    return "http://" + proxy

def delete_proxy(proxy):
    print('Proxy invalid: ' + proxy + '\n')
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def new_request(request, invalid_proxy=''):
    request.headers['User-Agent'] = random.choice(user_agents)
    request.headers[':authority'] = 'www.amazon.com'
    request.headers[':method'] = 'GET'
    request.headers[':path'] = '/dp/B003AI2VGA'
    request.headers[':scheme'] = 'https'
    request.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    request.headers['accept-encoding'] = 'gzip, deflate, br'
    request.headers['accept-language'] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    request.headers['cache-control'] = 'no-cache'
    request.meta['proxy'] = proxy()
    if 'retry_times' in request.meta.keys():
        request.meta['retry_times'] += 1
    else:
        request.meta['retry_times'] = 0
    if invalid_proxy != '':
        delete_proxy(invalid_proxy)
    return request