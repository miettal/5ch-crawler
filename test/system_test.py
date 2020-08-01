import scrapy.crawler

from gochan_crawler.spiders.board import BoardSpider
from gochan_crawler.spiders.board_list import BoardListSpider
from gochan_crawler.spiders.thread import ThreadSpider


def test_board_list():
    crawler_process = scrapy.crawler.CrawlerProcess()
    crawler_process.crawl(BoardListSpider)
    crawler_process.start(stop_after_crawl=False)
    # def test_board():
    crawler_process = scrapy.crawler.CrawlerProcess()
    crawler_process.crawl(BoardSpider, url='https://asahi.5ch.net/newsplus/')
    crawler_process.start(stop_after_crawl=False)
    # def test_thread():
    crawler_process = scrapy.crawler.CrawlerProcess()
    crawler_process.crawl(ThreadSpider, url='https://asahi.5ch.net/test/read.cgi/newsplus/1596266486/l50')
    crawler_process.start(stop_after_crawl=False)

# runner = CrawlerRunner()
# d = runner.crawl(ThreadSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run()
