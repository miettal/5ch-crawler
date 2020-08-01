# -*- coding: utf-8 -*-
import scrapy


class BoardListSpider(scrapy.Spider):
    name = 'board_list'
    allowed_domains = ['5ch.net']
    start_urls = ['https://menu.5ch.net/bbstable.html']

    def parse(self, response):
        board_category = None
        for e in response.css('table > tr >td > font > a, table > tr > td > font > b'):
            try:
                board_category = e.css('b::text').extract()[0]
                print(board_category)
                continue
            except IndexError:
                pass
            if board_category is None:
                continue
            board_name = e.css('a::text').extract()[0]
            board_url = e.css('a::attr("href")').extract()[0]
            yield {
                'category': board_category,
                'name': board_name,
                'url': board_url,
            }
