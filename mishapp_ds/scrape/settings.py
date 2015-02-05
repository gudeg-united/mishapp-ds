# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

BOT_NAME = 'mishapp_ds'
SPIDER_MODULES = ['mishapp_ds.scrape.spiders']
NEWSPIDER_MODULE = 'mishapp_ds.scrape.spiders'
USER_AGENT = 'mishapp_ds (+http://mishapp.com)'

ITEM_PIPELINES = {
    "mishapp_ds.scrape.pipelines.RedisPubsubPipeline": 20,
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware": 950,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60 * 30

REDIS_URI = "redis://localhost/0"
