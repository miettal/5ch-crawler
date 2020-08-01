
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner

from gochan_crawler.spiders.thread import ThreadSpider


def test_system():
    runner = CrawlerRunner()
    d = runner.crawl(ThreadSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
