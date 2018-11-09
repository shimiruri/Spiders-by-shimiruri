# -*- coding: utf-8 -*-

# Scrapy settings for bilibili project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from cookies import bilibili
import json
import random
from fake_useragent import UserAgent

BOT_NAME = 'bilibili'

SPIDER_MODULES = ['bilibili.spiders']
NEWSPIDER_MODULE = 'bilibili.spiders'


def get_cookies():
    bilibili.BiliBili().crack('username', 'password')
    cookies_dict = dict()
    with open("D:/ScrapySpider/bilibili/cookies.txt", 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict


COOKIE = get_cookies()

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = UserAgent().random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.randint(1, 3) + random.random()
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Referer': 'https://space.bilibili.com/4787127/',
    'Connection': 'keep-alive'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bilibili.middlewares.BilibiliSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'bilibili.middlewares.ProxyMiddleware': 553,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bilibili.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Use scrapy-redis dupefilter
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Use scrapy-redis scheduler
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# Permit save schedule after mission suspend
SCHEDULER_PERSIST = True

# Choice queue
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# Set redis information
REDIS_URL = 'redis://192.168.1.104:6379'

# Set mongodb information
MONGO_URI = 'mongodb://192.168.1.103:27017'
MONGO_DB = 'bilibili'

# Set proxy url
PROXY_URL = 'http://127.0.0.1:5555/random'



