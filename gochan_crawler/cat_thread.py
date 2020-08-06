import json
from optparse import OptionParser
import re

from scrapy import crawler
from scrapy import signals
from scrapy.signalmanager import dispatcher

from gochan_crawler.spiders.thread import ThreadSpider


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--pattern', dest='pattern')
    parser.add_option('-u', '--url', dest='url')
    (options, args) = parser.parse_args()

    posts = []

    def crawler_results(signal, sender, item, response, spider):
        """crawler_results."""
        posts.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    crawler_process = crawler.CrawlerProcess({
        'LOG_LEVEL': 'WARNING',
    })
    crawler_process.crawl(ThreadSpider, url=options.url)
    crawler_process.start()

    for post in posts:
        m = re.search(options.pattern, post['message_text'])
        if m:
            json.dumps(post)
