# -*- coding: utf-8 -*-
import datetime
import re

import pytz

import scrapy


class DrilldownSpider(scrapy.Spider):
    name = 'drilldown'
    allowed_domains = ['5ch.net']
    start_urls = ['http://menu.5ch.net/bbstable.html']

    def __init__(self, board_name, thread_title, post_message):
        self.board_name = board_name
        self.thread_title = thread_title
        self.post_message = post_message

    def parse(self, response):
        board_category = None
        for e in response.css('table > tr >td > font > a, table > tr > td > font > b'):
            try:
                board_category = e.css('b::text').extract()[0]
                continue
            except IndexError:
                pass
            if board_category is None:
                continue
            board_name = e.css('a::text').extract()[0]
            board_url = e.css('a::attr("href")').extract()[0]

            m = re.search(self.board_name, board_name)
            if m:
                yield scrapy.Request(
                    '{:s}/subback.html'.format(response.urljoin(board_url)),
                    callback=self.parse_board,
                    meta={
                        'board': {
                            'category': board_category,
                            'name': board_name,
                            'url': board_url,
                        },
                    }
                )

    def parse_board(self, response):
        m = re.match('(https?://[a-zA-Z0-9]+\\.5ch\\.net)/([a-zA-Z0-9]+)(/.*)?', response.url)
        if m is None:
            raise Exception()
        board_server = m.group(1)
        board_name = m.group(2)

        for a in response.css('#trad a'):
            thread_id = a.css('a::attr("href")').re('([0-9]+)/l50')[0]
            thread_title = a.css('a::text').re('[0-9]+: (.+) \\([0-9]+\\)')[0]
            thread_url = '{:s}/test/read.cgi/{:s}/{:s}/'.format(board_server, board_name, thread_id)

            m = re.search(self.thread_title, thread_title)
            if m:
                yield scrapy.Request(
                    response.urljoin(thread_url),
                    callback=self.parse_thread,
                    meta={
                        'board': response.meta['board'],
                        'thread': {
                            'id': thread_id,
                            'url': thread_url,
                            'title': thread_title,
                        },
                    }
                )

    def parse_thread(self, response):
        for div in response.css('.thread .post'):
            post_id = int(div.css('.number::text').extract()[0])
            post_url = '{:s}/{:d}'.format(response.url, post_id)
            try:
                post_name = div.css('.name b a::text').extract()[0]
                post_mail = div.css('.name b a::attr("href")').extract()[0]
            except IndexError:
                post_name = div.css('.name b::text').extract()[0]
                post_mail = None
            post_date = div.css('.date::text').extract()[0]
            m = re.match('([0-9]{4})/([0-9]{2})/([0-9]{2})\\([日月火水木金土]\\) ([0-9]{2}):([0-9]{2}):([0-9]{2})\\.([0-9]{2})', post_date)
            if m:
                try:
                    post_date = datetime.datetime(
                        int(m.group(1)), int(m.group(2)), int(m.group(3)),
                        int(m.group(4)), int(m.group(5)), int(m.group(6)),
                        int(m.group(7)) * 1000 * 10,
                    )
                    tz = pytz.timezone('Asia/Tokyo')
                    post_date = tz.localize(post_date)
                except ValueError:
                    pass
            else:
                post_date = None
            try:
                post_uid = div.css('.uid::text').re('ID:(.+)')[0]
            except IndexError:
                post_uid = None
            post_message_html = div.css('.message').extract()[0]
            post_message_text = post_message_html
            while True:
                m = re.search('( <br>)+ ', post_message_text)
                if m is None:
                    break
                c = m.group(0).count('br')
                post_message_text = re.sub('( <br>)+ ', '\n' * c, post_message_text, count=1, flags=re.DOTALL)
            post_message_text = re.sub('<[^>]*>', '', post_message_text, flags=re.DOTALL)

            m = re.search(self.post_message, post_message_text)
            if m:
                yield {
                    'board': response.meta['board'],
                    'thread': response.meta['thread'],
                    'post': {
                        'id': post_id,
                        'url': post_url,
                        'name': post_name,
                        'mail': post_mail,
                        'date': post_date,
                        'uid': post_uid,
                        'message_html': post_message_html,
                        'message_text': post_message_text,
                    },
                }
