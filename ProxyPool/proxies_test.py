from proxies_storage import RedisClient
from proxies_settings import valid_status, test_url, max_test_count
import asyncio
import aiohttp
import time


class Test(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_one_proxy(self, proxy):
        """
        Test one proxy.
        :param proxy: Proxy of waiting for testing.
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                full_proxy = 'http://' + proxy
                print("Proxy:{} is Testing.".format(full_proxy))
                async with session.get(test_url, proxy=full_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status == valid_status:
                        self.redis.set_max(proxy)
                        print("Proxy:{} can use!!!".format(proxy))
                    else:
                        self.redis.decrease(proxy)
                        print("Response code is Invalid!!!", proxy, " cannot be used.")
            except (aiohttp.ClientError, asyncio.TimeoutError, aiohttp.ClientConnectorError, aiohttp.ServerTimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print("Proxy:{} Request Failed!!!".format(proxy))

    def run(self):
        """
        Main function of testing.
        :return: None
        """
        print("Tester start to Run!!!")
        try:
            proxies = self.redis.all_proxies()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), max_test_count):
                test_proxies = proxies[i: i + max_test_count]
                tasks = [self.test_one_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("Test Displayed Error:", e)


