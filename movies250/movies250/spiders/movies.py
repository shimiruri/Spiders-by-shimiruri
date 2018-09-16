# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from movies250.items import *
from scrapy.http import Request


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['movie.douban.com']
    first_url = 'https://movie.douban.com/top250?start=0&filter='
    rules = (
        Rule(LinkExtractor(allow=r'.*/subject/\d+/$', restrict_xpaths="//ol[@class='grid_view']/li/div/div[2]"),
             callback='parse_comment'),
        Rule(LinkExtractor(restrict_xpaths="//span[@class='next']/a[contains(., '后页')]"), callback='parse_start_url',
             follow=True),
    )
    headers = {
        'Connection': 'keep - alive'
    }
    cookies = 'cookie'

    def start_requests(self):
        yield Request(url=self.first_url, headers=self.headers, cookies=self.cookies)
    
    def parse_start_url(self, response):
        infos = response.xpath("//div[@class='info']")
        for info in infos:
            item = SurfaceItem()
            item['name'] = info.xpath("div[1]/a/span[1]/text()").extract_first()
            item['score'] = info.xpath("div[2]/div/span[2]/text()").extract_first()
            item['quote'] = info.xpath("div[2]/p[2]/span/text()").extract_first()
            item['url'] = info.xpath("div[1]/a/@href").extract_first()
            yield item

    def parse_comment(self, response):
        if response.xpath("//div[@class='indent']/span[@class='all hidden']"):
            movie_introduce = response.xpath("//div[@class='indent']/span[@class='all hidden']//text()").extract_first().strip()
        else:
            movie_introduce = response.xpath("//div[@class='indent']/span[@property]//text()").extract_first().strip()
        comment_url = response.xpath("//div[@id='comments-section']/div[@class='mod-hd']/h2/span/a/@href").extract_first()
        yield Request(url=comment_url, callback=self.parse_reviews, headers=self.headers, cookies=self.cookies,
                      meta={"movie_introduce": movie_introduce, "comment_url": comment_url})

    def parse_reviews(self, response):
        item = CommentItem()   
        item['review_content'] = {}     
        contents = response.xpath("//div[@class='mod-bd' and @id='comments']/div[@class='comment-item']/div[@class='comment']")
        for content in contents:
            author = content.xpath("h3/span[2]/a/text()").extract_first()
            review = content.xpath("p/span/text()").extract_first()
            item['review_content'][author] = review    
        item['movie_introduce'] = response.meta.get('movie_introduce')
        item['comment_url'] = response.meta.get('comment_url')
        yield item
