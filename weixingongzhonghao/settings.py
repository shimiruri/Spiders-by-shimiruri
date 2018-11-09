# -*- coding: utf-8 -*-

# Scrapy settings for weixingongzhonghao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
import random

BOT_NAME = 'weixingongzhonghao'

SPIDER_MODULES = ['weixingongzhonghao.spiders']
NEWSPIDER_MODULE = 'weixingongzhonghao.spiders'


def cookies(cookie):
    cookie_dict = {}
    for i in cookie.split(';'):
        key = i.split('=')[0].raplace(" ", "")
        value = i.split('=')[1]
        cookie_dict[key] = value
        return cookie_dict


COOKIES = cookies('SUV=00EC599C74C034EB5BD822E7EA16B434; ABTEST=4|1541068692|v1; IPLOC=CN3100; SUID=752CAD3D3E18960A000000005BDAD794; SUID=752CAD3D2D18960A000000005BDAD795; weixinIndexVisited=1; sct=1; JSESSIONID=aaanZfipUd_x1eQBf2-Aw; ppinf=5|1541079396|1542288996|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTUlQkYlOTclRTYlOUQlOTElRTUlQjklQjMlRTclQTclODB8Y3J0OjEwOjE1NDEwNzkzOTZ8cmVmbmljazozNjolRTUlQkYlOTclRTYlOUQlOTElRTUlQjklQjMlRTclQTclODB8dXNlcmlkOjQ0Om85dDJsdUFTN21ZWkdkblVwWlE5Z2d2MVlzUG9Ad2VpeGluLnNvaHUuY29tfA; pprdig=TcQAH044KmvZwQCjqCALcuD39ynI1Dq3SrgsntRZAtEedW2d7Yv-qkGcD8IalAE5W3_ooWDRAbs2_ah8nrVFyEq7LmJ_b7dbLDwh1AMnYOQggnxlm3mAxVRyidSWg-EAKBfQwkTM7wTTAgjJcPiEB9RijoZ9oaM-rxT_iDzG7Vo; sgid=01-32628913-AVvbAWTLAEhOuC6TNkyFR38; CXID=9131843DEAB2534E02B218A3273ACB22; ad=i4qTYyllll2bcfyulllllVs0Ipllllll5z17Nyllllwllllljllll5@@@@@@@@@@; SNUID=3B62E2724F4B3569ECD5AE9A4F593BC1; ppmdig=1541688770000000ce623aafd4976e379a03be37d38754c1')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = UserAgent().random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.random() + random.randint(1, 3)
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Connection': 'keep-alive',
   'Referer': 'https://weixin.sogou.com/weixin?query=python&type=2&page=12&ie=utf8'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weixingongzhonghao.middlewares.WeixingongzhonghaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'weixingongzhonghao.middlewares.ProxyMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'weixingongzhonghao.pipelines.MongoPipeline': 300,
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

# Set scrapy-redis settings
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'


# Set basic information for crawler.
REDIS_URL = 'redis://192.168.1.104:6379'
PROXY_URL = 'http://127.0.0.1:5556/random'
MONGO_URI = 'mongodb://192.168.1.103:27017'
MONGO_DB = 'weixin'