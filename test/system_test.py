
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner

from gochan_crawler.spiders.thread import ThreadCrawler


def test_system():
    runner = CrawlerRunner()
    d = runner.crawl(ThreadCrawler)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
