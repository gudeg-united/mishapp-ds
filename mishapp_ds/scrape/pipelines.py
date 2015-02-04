# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy.signals
from scrapy.exceptions import NotConfigured
from mongoengine import connect as mongo_connect


class MongoPipeline(object):
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self._conn = None

    @property
    def conn(self):
        if not self._conn:
            self._conn = mongo_connect(host=self.mongo_uri)
        return self._conn

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri = crawler.settings.get("MONGO_URI")

        if not mongo_uri:
            raise NotConfigured()

        pipeline = cls(mongo_uri)
        crawler.signals.connect(pipeline.spider_opened,
                                signal=scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,
                                signal=scrapy.signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        spider.log("starting mongo pipeline")

    def spider_closed(self, spider):
        spider.log("closing mongo pipeline")

    def process_item(self, item, spider):
        return item
