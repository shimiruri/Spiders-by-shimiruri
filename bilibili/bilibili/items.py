# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    collection = table = 'user_information'
    username = scrapy.Field()
    sex = scrapy.Field()
    vip = scrapy.Field()
    regtime = scrapy.Field()
    gamelist = scrapy.Field()
    fans = scrapy.Field()
