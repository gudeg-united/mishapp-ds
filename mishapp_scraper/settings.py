# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

BOT_NAME = 'mishapp_scraper'
SPIDER_MODULES = ['mishapp_scraper.spiders']
NEWSPIDER_MODULE = 'mishapp_scraper.spiders'
USER_AGENT = 'mishapp_scraper (+http://mishapp.com)'

ITEM_PIPELINES = {
    "mishapp_scraper.pipelines.MongoPipeline": 20,
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware": 950,
}

HTTPCACHE_ENABLED = os.environ.get("HTTPCACHE_ENABLED", True)
HTTPCACHE_EXPIRATION_SECS = 60 * 30
