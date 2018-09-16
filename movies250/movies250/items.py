# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SurfaceItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    quote = scrapy.Field()
    url = scrapy.Field()


class CommentItem(scrapy.Item):
    movie_introduce = scrapy.Field()
    comment_url = scrapy.Field()
    review_content = scrapy.Field()
