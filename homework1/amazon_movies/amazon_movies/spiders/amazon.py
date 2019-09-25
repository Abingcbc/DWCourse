# -*- coding: utf-8 -*-
import scrapy
from amazon_movies.items import AmazonMoviesItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def parse(self, response):
        if response.selector.xpath('')
