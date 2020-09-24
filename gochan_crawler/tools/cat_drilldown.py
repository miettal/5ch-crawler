import json
from optparse import OptionParser
from datetime import datetime
from datetime import date

from scrapy import crawler
from scrapy import signals
from scrapy.signalmanager import dispatcher

from gochan_crawler.spiders.drilldown import DrilldownSpider

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--board_name', dest='board_name')
    parser.add_option('--thread_title', dest='thread_title')
    parser.add_option('--post_message', dest='post_message')
    (options, args) = parser.parse_args()

    items = []

    def crawler_results(signal, sender, item, response, spider):
        """crawler_results."""
        items .append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    crawler_process = crawler.CrawlerProcess({
        'LOG_LEVEL': 'WARNING',
        'DOWNLOAD_TIMEOUT': 2,
    })
    crawler_process.crawl(DrilldownSpider, board_name=options.board_name, thread_title=options.thread_title, post_message=options.post_message)
    crawler_process.start()

    for item in items:
        print(json.dumps(item, default=json_serial))
