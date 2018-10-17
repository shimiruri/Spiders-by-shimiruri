from multiprocessing.dummy import Pool as ThreadPool
import re
import requests
from lxml import etree
import pymysql


class QianCheng(object):
    """Get jobs' information what your need from 51job."""
    def __init__(self, keyword):
        """
        :param keyword: The keyword what you want to search.
        """
        self.keyword = keyword
        self.start_url = "https://search.51job.com/list/020000%252C00,000000,0000,00,9,99," + self.keyword + ",2,1.html"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.db = MySQL("51job")
        self.pool = ThreadPool(6)

    def request(self, url):
        """Request object url and return its response.
        :param url: Object url.
        :return: Its response.
        """
        response = requests.get(url, headers=self.headers)
        response = response.content.decode("GBK")
        return response
    
    def parse(self, response):
        """To parse responses.
        :param response: Each response from the request.
        :return: All pages about keyword.
        """
        html = etree.HTML(response)
        pages = int(re.findall('共(\d+)页，到第', response)[0])
        results = html.xpath('//div[@id="resultList"]/div[@class="el"]')
        for result in results:
            position = result.xpath('p/span/a/@title')[0]
            detail_page = result.xpath('p/span/a/@href')[0]
            company = result.xpath('span[@class="t2"]/a/text()')[0]
            address = result.xpath('span[@class="t3"]/text()')[0]
            salary = result.xpath('span[@class="t4"]/text()')
            if len(salary) == 0:
                salary = '尚未公布'
            self.db.insert((position, detail_page, company, address, salary))
        return pages

    def all_responses(self):
        self.db.create()
        pages = self.parse(self.request(self.start_url))
        if pages == 1:
            self.db.close()
            print("Information has been saved!!!")
        else:
            urls = ["https://search.51job.com/list/020000%252C00,000000,0000,00,9,99," + self.keyword + ",2,%s.html"
                    % (page) for page in range(2, pages + 1)]
            responses = self.pool.map(self.request, urls)
            self.pool.close()
            self.pool.join()
            # It can also use threading.
            for response in list(responses):
                self.parse(response)
            self.db.close()
            print("All information has been saved!!!")


class MySQL(object):
    """Save information into Mysql."""
    def __init__(self, dbname):
        """Basic of class params.Pay attention to adding db params 'charset'.
        :param dbname: Set a name of database.
        """
        db = pymysql.connect(host='your host', user='your name', password='your password', port='your port number', charset='utf8')
        db.cursor().execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8" % dbname)
        self.db = pymysql.connect(host='your host', user='your name', password='your password', port='your port number', charset='utf8', db=dbname)
        self.cursor = self.db.cursor()
        self.dbname = dbname

    def create(self):
        self.cursor.execute("USE %s" % self.dbname)
        sql = "CREATE TABLE IF NOT EXISTS jobs(" \
              "id INT NOT NULL AUTO_INCREMENT, " \
              "position VARCHAR(255) NOT NULL, " \
              "detail_page VARCHAR(255) NOT NULL, " \
              "company VARCHAR(255) NOT NULL, " \
              "address VARCHAR(255) NOT NULL, " \
              "salary VARCHAR(255) NOT NULL, " \
              "PRIMARY KEY (id))"
        self.cursor.execute(sql)

    def insert(self, args):
        sql = "INSERT INTO jobs(position, detail_page, company, address, salary) VALUES(%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.db.close()


if __name__ == "__main__":
    q = QianCheng("爬虫")
    q.all_responses()







