import redis
from random import choice
from proxies_settings import redis_host, redis_port, redis_passwd, redis_key
from proxies_settings import max_score, min_score, init_score


class RedisClient(object):
    def __init__(self):
        self.db = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_passwd, decode_responses=True)

    def add(self, proxy):
        """
        Add new proxy into zset.
        :param proxy: New proxy.
        :return: Result of adding new proxy.
        """
        if not self.db.zscore(redis_key, proxy):
            return self.db.zadd(redis_key, init_score, proxy)

    def random(self):
        """
        Choice a max score proxy, but it is not existed, it must get proxy by ranking.
        :return: Proxy
        """
        result = self.db.zrangebyscore(redis_key, max_score, max_score)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(redis_key, min_score, max_score)
            if len(result):
                return choice(result)
            else:
                print("Proxy Pool has been Empty!!!")
                exit(0)

    def decrease(self, proxy):
        """
        Proxy score decrease one point. If proxy is not existed, delete it.
        :param proxy: Proxy
        :return: Changed score.
        """
        score = self.db.zscore(redis_key, proxy)
        if score and score > min_score:
            print("Proxy:", proxy, "; Score:", score, ' need -1.!!!')
            return self.db.zincrby(redis_key, proxy, -1)
        else:
            print("Proxy:", proxy, "; Score:", score, ' need Delete.')
            return self.db.zrem(redis_key, proxy)

    def exist(self, proxy):
        """
        Judge if proxy is existed in pool.
        :param proxy: Proxy
        :return: Result of proxy
        """
        return not self.db.zscore(redis_key, proxy) == None

    def set_max(self, proxy):
        """
        Set proxy to max score.
        :param proxy: Proxy
        :return: Result of setting max score
        """
        print("Proxy:", proxy, " can use normally! Set its score to ", max_score)
        return self.db.zadd(redis_key, max_score, proxy)

    def count(self):
        """
        Count number of proxies.
        :return: Count number.
        """
        return self.db.zcard(redis_key)

    def all_proxies(self):
        """
        Get all proxies from redis-zset.
        :return: All proxies.
        """
        return self.db.zrangebyscore(redis_key, min_score, max_score)
