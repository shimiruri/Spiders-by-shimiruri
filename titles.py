# coding = utf-8
import threading
import queue
import time
import requests
from lxml import etree
import pymongo


def produter(urlQueue):
    """获取网页源码
    :param urlQueue: 保存url的队列
    :return:
    """
    while True:
        try:
            url = urlQueue.get(False)
            print("当前线程是：%s, url是：%s" % (threading.current_thread().name, url))
            response = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
            if response.status_code == 200:
                dataQUEUE.put(response.text)
                time.sleep(1)
        except:
            break


def costumer(dataQueue, lock):
    """对响应进行解析并保存至数据库
    :param dataQueue: 存储响应的队列
    :param lock: 线程锁。用于同步线程，保证写数据时的稳定
    :return:
    """
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['titles']
    col = db['title']
    while True:
        try:
            html = etree.HTML(dataQueue.get(False))
            print("当前线程为：{}，正在保存网页信息···".format(threading.current_thread().name))
            page = html.xpath('//div[@id="pages"]/span/text()')[0]
            title = html.xpath('//ul[@id="catlist"]/li/a//h2/text()')
            item = {"page": page, "title": title}
            with lock:
                col.insert_one(item)
                # file.write(json.dumps(item, ensure_ascii=False) + ',' + '\n')
        except:
            break


if __name__ == '__main__':
    baseURL = "http://www.pythontab.com/html/pythonjichu/"
    urlQUEUE = queue.Queue()
    dataQUEUE = queue.Queue()
    lock = threading.Lock()

    # 为url队列添加元素
    for i in range(2, 10):
        url = baseURL + str(i) + '.html'
        urlQUEUE.put(url)

    start = time.time()

    # 网页采集使用多线程
    crawl_threads = []
    thread_num = 4
    for i in range(thread_num):
        t = threading.Thread(target=produter, args=(urlQUEUE,))
        crawl_threads.append(t)
        t.start()

    for thread in crawl_threads:
        thread.join()
    print("\n数据已存入队列！\n")

    # 解析响应并保存使用多线程
    print("开始解析网页并存储数据")
    parse_threads = []
    for i in range(thread_num):
        t = threading.Thread(target=costumer, args=(dataQUEUE, lock,))
        parse_threads.append(t)
        t.start()

    for thread in parse_threads:
        thread.join()

    end = time.time()
    print("执行完毕，耗时：", end - start)








