import json
from optparse import OptionParser
import re

from scrapy import crawler
from scrapy import signals
from scrapy.signalmanager import dispatcher

from gochan_crawler.spiders.board import BoardSpider


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--pattern', dest='pattern')
    parser.add_option('-u', '--url', dest='url')
    (options, args) = parser.parse_args()

    threads = []

    def crawler_results(signal, sender, item, response, spider):
        """crawler_results."""
        threads.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    crawler_process = crawler.CrawlerProcess({
        'LOG_LEVEL': 'WARNING',
    })
    crawler_process.crawl(BoardSpider, url=options.url)
    crawler_process.start()

    for thread in threads:
        m = re.search(options.pattern, thread['title'])
        if m:
            json.dumps(thread)
