# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy.signals


class MongoPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
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
