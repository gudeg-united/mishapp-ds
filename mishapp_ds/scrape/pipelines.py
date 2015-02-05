# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

import scrapy.signals
from scrapy.exceptions import NotConfigured
from redis.utils import from_url as redis_from_url


class RedisPubsubPipeline(object):
    def __init__(self, redis_uri):
        self.redis_uri = redis_uri
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = redis_from_url(self.redis_uri)
        return self._client

    @classmethod
    def from_crawler(cls, crawler):
        redis_uri = crawler.settings.get("REDIS_URI")

        if not redis_uri:
            raise NotConfigured()

        pipeline = cls(redis_uri)
        crawler.signals.connect(pipeline.spider_opened,
                                signal=scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,
                                signal=scrapy.signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        spider.log("starting redis pubsub pipeline")

    def spider_closed(self, spider):
        spider.log("closing redis pubsub pipeline")

    def process_item(self, item, spider):
        spider.log("publishing item through redis pubsub")
        self.client.publish("mishapp-datasource", json.dumps(dict(item)))
        return item
