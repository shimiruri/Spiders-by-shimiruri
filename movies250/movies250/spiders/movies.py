# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from movies250.items import *
from scrapy.http import Request


cookie = [
    'll="108289"',
    ' bid=4tzTVwG1T5M',
    ' _ga=GA1.2.1575338880.1521202914',
    ' __utmv=30149280.17547',
    ' __yadk_uid=sjNs7zNQGluwdU1mhuVlH78XVEGLbDEb',
    ' _vwo_uuid_v2=DA5252EF0963EB3E0F5423AFBEDE747DD|d1fdfc0ae134ebf81698c9c0cc347ec2',
    ' __utmz=223695111.1525616195.7.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    ' viewed="1019568"',
    ' gr_user_id=bccc63b1-cfba-4e6d-aeb9-92c028c1cc8a',
    ' __utmz=30149280.1533220063.11.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    ' ct=y',
    ' ps=y',
    ' ue="2847486314@qq.com"',
    ' push_noty_num=0',
    ' push_doumail_num=0',
    ' ap_v=1,6.0',
    ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1535552748%2C%22http%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DDKeKBDmAOO'
    'AT2ayZQO5OO52nukw3OVjLD1SFcWvVQgpWzMC_uAfvgeVgMeehBQsv%26wd%3D%26eqid%3Dc8e09b2600095e1e000000035aeef37f%22%5D',
    ' _pk_ses.100001.4cf6=*',
    ' __utma=30149280.1575338880.1521202914.1535470544.1535552750.15',
    ' __utmb=30149280.0.10.1535552750',
    ' __utmc=30149280',
    ' __utma=223695111.1575338880.1521202914.1535470544.1535552750.11',
    ' __utmb=223695111.0.10.1535552750',
    ' __utmc=223695111',
    ' _pk_id.100001.4cf6=d0208047fbc69b83.1524143613.11.1535553146.1535471180.',
    ' dbcl2="175472122:SkJEeWsWaFI"'
]
itemDict = {}
for item in cookie:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value


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
    cookies = itemDict

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