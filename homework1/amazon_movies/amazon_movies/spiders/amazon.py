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

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = []
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        count = 0
        with open('movies_id.txt', 'r') as file:
            for line in file:
                if count >= 1:
                    break
                if len(line.strip()) == 0:
                    continue
                self.start_urls.append('https://'+self.allowed_domains[0]+'/dp/'+line.strip())
                count += 1

    def parse(self, response):
        item = AmazonMoviesItem()
        item['ID'] = response.url
        item['ID'] = item['ID'].split('/')[-1].strip()
        response = BeautifulSoup(response.body, 'lxml')
        # If this film is banned by robot check, try it again.
        if not response.find(name='title', text=re.compile('Robot Check')) is None:
            print ('\nRobot check triggered\n')
            try_again = Request('https://www.amazon.com/dp/'+item['ID'], callback=self.parse)
            try_again.headers['User-Agent'] = random.choice(self.user_agents)
            try_again.meta['proxy'] = 'http://'+ \
                eval(requests.get("http://127.0.0.1:5010/get/").text)['proxy']
            yield try_again
        else:
            page_type = response.find(id='productTitle')
            if page_type is None:
                print('-'*10 + item['ID'] + ': Prime' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = prime_parser.prime_parse(response, item['ID'])
                yield item
            else:
                print('-'*10 + item['ID'] + ': Ordinary' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = ordinary_parser.ordinary_parse(response, item['ID'])
                yield item

        
