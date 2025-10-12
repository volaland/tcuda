# Scrapy settings for missilery_scraper project

BOT_NAME = 'missilery_scraper'

SPIDER_MODULES = ['missilery_scraper.spiders']
NEWSPIDER_MODULE = 'missilery_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure delays for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# Configure concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure user agent
USER_AGENT = 'missilery_scraper (+http://www.yourdomain.com)'

# Configure pipelines
ITEM_PIPELINES = {
    'missilery_scraper.pipelines.DataSeparationPipeline': 300,
}

# Configure logging
LOG_LEVEL = 'INFO'

# Configure retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Configure download timeout
DOWNLOAD_TIMEOUT = 30

# Configure cookies
COOKIES_ENABLED = True

# Configure headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
