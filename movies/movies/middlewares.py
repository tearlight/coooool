# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from random import choice
from settings import USER_AGENT_LIST
from helper import gen_bids
from scrapy.exceptions import IgnoreRequest
import redis
import settings


class MoviesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgent(object):

   def process_request(self,request,spider):

      ua = random.choice(USER_AGENT_LIST) 
      if ua:
         request.headers.setdefault('User-Agent',ua)

class CustomCookieMiddleware(object):

    def __init__(self):
       self.bids = gen_bids()

    def process_request(self,request,spider):
       request.headers['Cookie'] = 'bid="%s"' % choice(self.bids)

class InsertRedis(object):
    def __init__(self):
       self.Redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,db=settings.REDIS_DB)
       self.redis_key = settings.REDIS_KEY
    
    def process_request(self,request,spider):
       if self.Redis.sismember(self.redis_key,request.url):
          raise IgnoreRequest("IgnoreRequest : %s" % request.url)
       else:
          self.Redis.sadd(self.redis_key,request.url)
