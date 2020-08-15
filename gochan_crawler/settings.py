BOT_NAME = 'gochan_crawler'

SPIDER_MODULES = ['gochan_crawler.spiders']
NEWSPIDER_MODULE = 'gochan_crawler.spiders'


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
RETRY_TIMES = 5
DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 1
