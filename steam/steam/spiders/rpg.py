# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from steam.items import *


class RpgSpider(CrawlSpider):
    name = 'rpg'
    allow_domains = ["store.steampowered.com"]
    start_urls = ['https://store.steampowered.com/search/?sort_by=Reviews_DESC&tags=122&filter=topsellers']
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='search_pagination_right']/a[contains(., '>')]"),
             callback='parse_start_url', follow=True),
    )

    def _build_request(self, rule, link):
        r = Request(url=link.url, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text, dont_filter=True, dont_redirect=True, handle_httpstatus_list=[302])
        return r

    def parse_start_url(self, response):
        games = response.xpath("//div[@id='search_result_container']/div[2]/a")
        for game in games:
            item = SteamItem()
            item['name'] = game.xpath("div[2]/div[1]/span/text()").extract_first()
            item['evaluation'] = game.xpath("div[2]/div[3]/span/@data-tooltip-html").extract_first()
            item['url'] = game.xpath("@href").extract_first()
            if game.xpath("div[2]/div[4]/div[1]/span"):
                item['price'] = game.xpath("div[2]/div[4]/div[2]/text()[2]").re_first("(¥ \d*)")
            else:
                item['price'] = game.xpath("div[2]/div[4]/div[2]/text()[1]").re_first("(¥ \d*)")
            yield item
   




        
        

            



        

        

