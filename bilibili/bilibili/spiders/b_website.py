# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from bilibili.items import BilibiliItem
from bilibili.settings import COOKIE
import json
import time


class BWebsiteSpider(Spider):
    name = 'b_website'
    allowed_domains = ['space.bilibili.com', 'api.bilibili.com']
    urls = [
        'https://space.bilibili.com/ajax/member/GetInfo',
        'https://api.bilibili.com/x/relation/stat?vmid=',
        'https://space.bilibili.com/ajax/game/GetLastPlay?mid='
    ]

    def __init__(self):
        self.cookies = COOKIE
        super(BWebsiteSpider, self).__init__()

    def start_requests(self):
        csrf = self.cookies.get('bili_jct')
        for i in range(1, 20000001):
            mid = str(i)
            form = {
                'mid': mid,
                'csrf': csrf
            }
            yield scrapy.FormRequest(
                url=self.urls[0], formdata=form, dont_filter=True,
                cookies=self.cookies,
                callback=self.get_basic_info, meta={'mid': mid}
            )

    def get_basic_info(self, response):
        infos = json.loads(response.text)
        mid = response.meta['mid']
        if infos.get('status') is True:
            data = infos.get('data')
            username = data.get('name')
            if data.get('sex') == '保密' or data.get('sex') is None:
                sex = '未知'
            else:
                sex = data.get('sex')
            vip = data.get('vip').get('vipStatus')
            regtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get('regtime')))
        else:
            print('用户信息采集失败')
        yield scrapy.Request(
            url=self.urls[1] + mid, cookies=self.cookies,
            callback=self.get_fans_num, meta={
                'mid': mid, 'username': username,
                'sex': sex, 'vip': vip, 'regtime': regtime
            }
        )

    def get_fans_num(self, response):
        infos = json.loads(response.text)
        mid = response.meta['mid']
        username = response.meta['username']
        sex = response.meta['sex']
        vip = response.meta['vip']
        regtime = response.meta['regtime']
        fans = infos.get('data').get('follower')
        yield scrapy.Request(
            url=self.urls[2] + mid, cookies=self.cookies,
            callback=self.parse, meta={
                'mid': mid, 'username': username, 'sex': sex,
                'vip': vip, 'regtime': regtime, 'fans': fans
            }
        )

    def parse(self, response):
        item = BilibiliItem()
        gamelists = json.loads(response.text)
        try:
            if gamelists.get('data').get('count') == 0:
                item['gamelist'] = 'No game!'
            else:
                item['gamelist'] = [i.get('name') for i in gamelists.get('data').get('games')]
        except:
            item['gamelist'] = gamelists.get('data')
        item['username'] = response.meta['username']
        item['sex'] = response.meta['sex']
        item['vip'] = response.meta['vip']
        item['regtime'] = response.meta['regtime']
        item['fans'] = response.meta['fans']
        yield item











