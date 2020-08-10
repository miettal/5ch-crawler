import json
from optparse import OptionParser
import re
from datetime import datetime
from datetime import date

from scrapy import crawler
from scrapy import signals
from scrapy.signalmanager import dispatcher

from gochan_crawler.spiders.board_list import BoardListSpider


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--pattern', dest='pattern')
    (options, args) = parser.parse_args()

    boards = []

    def crawler_results(signal, sender, item, response, spider):
        """crawler_results."""
        boards.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    crawler_process = crawler.CrawlerProcess({
        'LOG_LEVEL': 'WARNING',
    })
    crawler_process.crawl(BoardListSpider)
    crawler_process.start()

    for board in boards:
        m = re.search(options.pattern, board['name'])
        if m:
            print(json.dumps(board, default=json_serial))
