# -*- coding: utf-8 -*-
import datetime
import re

import pytz

import scrapy


class ThreadSpider(scrapy.Spider):
    name = 'thread'
    allowed_domains = ['5ch.net']

    def __init__(self, url=None):
        if url is None:
            raise Exception()
        m = re.match('(https?://[a-zA-Z0-9.]+/test/read.cgi/[a-zA-Z0-9]+/[0-9]+)(/.*)?', url)
        if m is None:
            raise Exception()
        self.thread_url = m.group(1)
        self.start_urls = [self.thread_url]

    def parse(self, response):
        for div in response.css('.thread .post'):
            post_id = int(div.css('.number::text').extract()[0])
            post_url = '{:s}/{:d}'.format(self.thread_url, post_id)
            try:
                post_name = div.css('.name b a::text').extract()[0]
                post_mail = div.css('.name b a::attr("href")').extract()[0]
            except IndexError:
                post_name = div.css('.name b::text').extract()[0]
                post_mail = None
            post_date = div.css('.date::text').extract()[0]
            m = re.match('([0-9]{4})/([0-9]{2})/([0-9]){2}\\([日月火水木金土]\\) ([0-9]{2}):([0-9]{2}):([0-9]{2})\\.([0-9]{2})', post_date)
            if m:
                post_date = datetime.datetime(
                    int(m.group(1)), int(m.group(2)), int(m.group(3)),
                    int(m.group(4)), int(m.group(5)), int(m.group(6)),
                    int(m.group(7)) * 1000 * 10,
                )
                tz = pytz.timezone('Asia/Tokyo')
                post_date = tz.localize(post_date)
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
            yield {
                'id': post_id,
                'url': post_url,
                'name': post_name,
                'mail': post_mail,
                'date': post_date,
                'uid': post_uid,
                'message_html': post_message_html,
                'message_text': post_message_text,
            }
