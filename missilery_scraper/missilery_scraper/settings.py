"""
Scrapy settings for missilery_scraper project.

This module imports all Scrapy configuration settings from the constants module
to maintain consistency and avoid duplication.
"""

from .constants import (
    BOT_NAME, SPIDER_MODULES, NEWSPIDER_MODULE, ROBOTSTXT_OBEY,
    DOWNLOAD_DELAY, RANDOMIZE_DOWNLOAD_DELAY, CONCURRENT_REQUESTS,
    CONCURRENT_REQUESTS_PER_DOMAIN, USER_AGENT, ITEM_PIPELINES,
    LOG_LEVEL, RETRY_TIMES, RETRY_HTTP_CODES, DOWNLOAD_TIMEOUT,
    COOKIES_ENABLED, DEFAULT_REQUEST_HEADERS
)

# Bot configuration
BOT_NAME = BOT_NAME  # pylint: disable=self-assigning-variable
SPIDER_MODULES = SPIDER_MODULES  # pylint: disable=self-assigning-variable
NEWSPIDER_MODULE = NEWSPIDER_MODULE  # pylint: disable=self-assigning-variable

# Obey robots.txt rules
ROBOTSTXT_OBEY = ROBOTSTXT_OBEY  # pylint: disable=self-assigning-variable

# Configure delays for requests for the same website (default: 0)
DOWNLOAD_DELAY = DOWNLOAD_DELAY  # pylint: disable=self-assigning-variable
RANDOMIZE_DOWNLOAD_DELAY = RANDOMIZE_DOWNLOAD_DELAY  # pylint: disable=self-assigning-variable

# Configure concurrent requests
CONCURRENT_REQUESTS = CONCURRENT_REQUESTS  # pylint: disable=self-assigning-variable
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS_PER_DOMAIN  # pylint: disable=self-assigning-variable

# Configure user agent
USER_AGENT = USER_AGENT  # pylint: disable=self-assigning-variable

# Configure pipelines
ITEM_PIPELINES = ITEM_PIPELINES  # pylint: disable=self-assigning-variable

# Configure logging
LOG_LEVEL = LOG_LEVEL  # pylint: disable=self-assigning-variable

# Configure retry settings
RETRY_TIMES = RETRY_TIMES  # pylint: disable=self-assigning-variable
RETRY_HTTP_CODES = RETRY_HTTP_CODES  # pylint: disable=self-assigning-variable

# Configure download timeout
DOWNLOAD_TIMEOUT = DOWNLOAD_TIMEOUT  # pylint: disable=self-assigning-variable

# Configure cookies
COOKIES_ENABLED = COOKIES_ENABLED  # pylint: disable=self-assigning-variable

# Configure headers
DEFAULT_REQUEST_HEADERS = DEFAULT_REQUEST_HEADERS  # pylint: disable=self-assigning-variable
