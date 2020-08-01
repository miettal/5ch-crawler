# -*- coding: utf-8 -*-
import re

import scrapy


class BoardSpider(scrapy.Spider):
    name = 'board'
    allowed_domains = ['5ch.net']

    def __init__(self, url='https://asahi.5ch.net/newsplus/'):
        m = re.match('(https?://[a-zA-Z0-9]+\\.5ch\\.net)/([a-zA-Z0-9]+)(/.*)?', url)
        if m is None:
            raise Exception()
        board_url = '{:s}/{:s}/subback.html'.format(m.group(1), m.group(2))
        self.board_server = m.group(1)
        self.board_name = m.group(2)
        self.start_urls = [board_url]

    def parse(self, response):
        for a in response.css('#trad a'):
            thread_id = a.css('a::attr("href")').re('([0-9]+)/l50')[0]
            thread_title = a.css('a::text').re('[0-9]+: (.+) \\([0-9]+\\)')[0]
            thread_url = '{:s}/test/read.cgi/{:s}/{:s}/'.format(self.board_server, self.board_name, thread_id)
            yield {
                'id': thread_id,
                'url': thread_url,
                'title': thread_title,
            }
