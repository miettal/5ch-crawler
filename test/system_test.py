import scrapy.crawler

from gochan_crawler.spiders.thread import ThreadSpider


def test_system():
    crawler_process = scrapy.crawler.CrawlerProcess()
    crawler_process.crawle(ThreadSpider, url='https://asahi.5ch.net/test/read.cgi/newsplus/1596266486/l50')
    crawler_process.start()

    # runner = CrawlerRunner()
    # d = runner.crawl(ThreadSpider)
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()
