# -*- coding: utf-8 -*-
import scrapy
from amazon_movies.items import AmazonMoviesItem
from bs4 import BeautifulSoup
import re
import amazon_movies.spiders.prime_parser as prime_parser
import amazon_movies.spiders.ordinary_parser as ordinary_parser
from amazon_movies.items import AmazonMoviesItem
import os
from scrapy.http import Request
import random
import requests
import amazon_movies.utils as utils
import urllib
from imageRecognize.imageRec import parse_robot
from amazon_movies.utils import *

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = []
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        with open('movies_id.txt', 'r') as file:
            count = 0
            for line in file:
                if count > 10:
                    break
                count += 1
                if len(line.strip()) == 0:
                    continue
                self.start_urls.append('https://'+self.allowed_domains[0]+'/dp/'+line.strip())

    def parse(self, response):
        item = AmazonMoviesItem()
        print('Get page ' + str(response.url))
        item['ID'] = response.url
        item['ID'] = item['ID'].split('/')[-1].strip()
        proxy = response.request.meta['proxy'].replace('http://','')
        content = BeautifulSoup(response.body, 'lxml')
        if response.status == 404:
            item['validation'] = False
            yield item
        # If this film is banned by robot check, try it again.
        elif not content.find(name='title', text=re.compile('Robot Check')) is None:
            print ('Robot check triggered')
            urllib.request.urlretrieve(content.find(name='div', attrs={'class':'a-row a-text-center'}).
            find(name='img',attrs={'src':True}), 'robot.jpg')
            capt_string = parse_robot('robot.jpg')
            if capt_string == "error":
                yield scrapy.Request(response.url, dont_filter=True)
            else:
                data = {'field-keywords': capt_string}
                yield scrapy.FormRequest.from_response(response, formdata=data, callback = self.parse, dont_filter=True)
        else:
            page_type = content.find(id='productTitle')
            if page_type is None:
                # print('-'*10 + item['ID'] + ': Prime' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = prime_parser.prime_parse(content, item['ID'])
                yield item
            else:
                # print('-'*10 + item['ID'] + ': Ordinary' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = ordinary_parser.ordinary_parse(content, item['ID'])
                yield item

        
