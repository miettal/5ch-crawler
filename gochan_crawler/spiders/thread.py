# -*- coding: utf-8 -*-
import scrapy


class ThreadSpider(scrapy.Spider):
    name = 'thread'
    allowed_domains = ['5ch.net']
    start_urls = ['http://5ch.net/']

    def parse(self, response):
        pass
