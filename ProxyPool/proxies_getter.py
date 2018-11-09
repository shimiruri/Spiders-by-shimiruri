from proxies_spider import ProxySpider
from proxies_storage import RedisClient


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.spider = ProxySpider()
        self.proxies_pool_threshold = 1000

    def judge_over_threshold(self):
        """
        Judge if proxies count is over threshold.
        :return: Result of judged.
        """
        if self.redis.count() >= self.proxies_pool_threshold:
            return True
        else:
            return False

    def get_proxies(self):
        """
        Get proxies and save them into redis.
        :return:None
        """
        print("Getter has been executed!!!")
        if not self.judge_over_threshold():
            for i in range(self.spider.__SpiderFuncCount__):
                callback = self.spider.__SpiderFunc__[i]
                proxies = self.spider.all_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
