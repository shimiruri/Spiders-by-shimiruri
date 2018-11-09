# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from weixingongzhonghao.items import WeixingongzhonghaoItem


class WeixinSpider(RedisCrawlSpider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    # start_urls = ['https://weixin.sogou.com/weixin?query=python&type=2&page=1&ie=utf8']
    redis_key = 'weixin:start_urls'

    rules = (
        # 翻页
        Rule(LinkExtractor(restrict_xpaths='//a[@id="sogou_next"]/@href'), follow=True),
        # 详情页
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="news-list"]/li/div[@class="txt-box"]/h3/a/@href'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = WeixingongzhonghaoItem()
        item['title'] = response.xpath('//h2/text()').extract_first().strip()
        item['datetime'] = response.xpath('//em/text()').extract_first()
        item['url'] = response.url
        item['source'] = response.xpath('//a[@id="js_name"]/text()').extract_first().strip()
        yield item



