"""
Scrapy middlewares for the Missilery scraper project.

This module contains custom spider and downloader middlewares that handle
request processing, response filtering, and data extraction optimization.
"""

from scrapy import signals


class MissileryScraperSpiderMiddleware:
    """Custom spider middleware for the Missilery scraper."""
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """Create spider middleware instance and connect signals."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):  # pylint: disable=unused-argument
        """Process spider input response."""
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):  # pylint: disable=unused-argument
        """Process spider output results."""
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        yield from result

    def process_spider_exception(self, response, exception, spider):  # pylint: disable=unused-argument
        """Process spider exceptions."""
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        """Process async start iterator."""
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        """Handle spider opened event."""
        spider.logger.info(f"Spider opened: {spider.name}")


class MissileryScraperDownloaderMiddleware:
    """Custom downloader middleware for the Missilery scraper."""
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """Create downloader middleware instance and connect signals."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):  # pylint: disable=unused-argument
        """Process download request."""
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):  # pylint: disable=unused-argument
        """Process download response."""
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):  # pylint: disable=unused-argument
        """Process download exceptions."""
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        """Handle spider opened event."""
        spider.logger.info(f"Spider opened: {spider.name}")
