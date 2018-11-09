import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent
from pyquery import PyQuery as pq


def request(url):
    """
    Request proxies information from other website.
    :param url: URL of proxy
    :return: Response of website
    """
    headers = {
        "User-Agent": UserAgent().random
    }
    print("Crawl Proxies From Website Now!!!")
    try:
        response = requests.get(url=url, headers=headers)
        print("Get Proxies Successfully!!!")
        return response.text
    except ConnectionError:
        print("Get Proxies Failed!!!")
        return None


class ProxyMetaclass(type):
    """
    Metaclass for proxy crawler,Set name format to use its method more convenient.
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__SpiderFunc__'] = []
        for k, v in attrs.items():
            if 'spider_' in k:
                attrs['__SpiderFunc__'].append(k)
                count += 1
        attrs['__SpiderFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxySpider(object, metaclass=ProxyMetaclass):
    def all_proxies(self, callback):
        """
        Get all proxies from all websites what you set.
        :param callback: Method of getting proxies.
        :return: All proxies.
        """
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print("Crawl Proxy:{} Successfully!!!".format(proxy))
            proxies.append(proxy)
        return proxies

    def spider_xicidaili(self):
        """
        Get proxies from xicidaili.
        :return: Generator of all proxies.
        """
        base_url = 'http://www.xicidaili.com/nn/{}'
        urls = [base_url.format(str(i)) for i in range(1, 4)]
        for url in urls:
            html = request(url=url)
            if html:
                doc = pq(html)
                ips = [ip.text for ip in doc('td:nth-child(2)')]
                ports = [port.text for port in doc('td:nth-child(3)')]
                for proxy in zip(ips, ports):
                    yield proxy[0] + ':' + proxy[1]

    def spider_kuaidaili(self):
        """
        Get proxies from kuaidaili.
        :return: Generator of proxies.
        """
        for i in range(1, 7):
            url = 'https://www.kuaidaili.com/free/inha/{}/'.format(str(i))
            html = request(url)
            if html:
                doc = pq(html)
                ips = [ip.text for ip in doc('td:first-child')]
                ports = [port.text for port in doc('td:nth-child(2)')]
                for proxy in zip(ips, ports):
                    yield proxy[0] + ':' + proxy[1]
