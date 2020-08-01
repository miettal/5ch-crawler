# -*- coding: utf-8 -*-
import re

import scrapy


class BoardSpider(scrapy.Spider):
    name = 'board'
    allowed_domains = ['5ch.net']

    def __init__(self, start_url='https://asahi.5ch.net/newsplus/'):
        m = re.match('(https?://)?([a-zA-Z0-9]+\\.5ch\\.net/[a-zA-Z0-9]+)(/.*)?', start_url)
        if m is None:
            raise Exception()
        url = 'https://{:s}/subback.html'.format(m.group(2))
        self.start_urls = [url]

    def parse(self, response):
        for a in response.css('#trad a'):
            thread_id = a.css('a::attr("href")').re('([0-9]+)/l50')[0]
            thread_title = a.css('a::text').re('[0-9]+: (.+) \\([0-9]+\\)')[0]
            yield {
                'id': thread_id,
                'title': thread_title,
            }
