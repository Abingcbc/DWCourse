# -*- coding: utf-8 -*-
import scrapy
from amazon_movies.items import AmazonMoviesItem
from bs4 import BeautifulSoup
import re
import amazon_movies.spiders.prime_parser as prime_parser
import amazon_movies.spiders.ordinary_parser as ordinary_parser
from amazon_movies.items import AmazonMoviesItem
import os

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        count = 0
        with open('movies_id.txt', 'r') as file:
            for line in file:
                if count > 10000:
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

        
