# coding = utf-8
import threading
import queue
import time
import requests
import json
from lxml import etree


# 生产者
def produter(urlQueue):
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


# 消费者
def costumer(file, dataQueue, lock):
    while True:
        try:
            html = etree.HTML(dataQueue.get(False))
            print("当前线程为：{}，正在保存网页信息···".format(threading.current_thread().name))
            page = html.xpath('//div[@id="pages"]/span/text()')[0]
            title = html.xpath('//ul[@id="catlist"]/li/a//h2/text()')
            item = {"page": page, "title": title}
            with lock:
                file.write(json.dumps(item, ensure_ascii=False) + ',' + '\n')
        except:
            break


if __name__ == '__main__':
    baseURL = "http://www.pythontab.com/html/pythonjichu/"
    urlQUEUE = queue.Queue()
    dataQUEUE = queue.Queue()
    file = open('titles.json', 'a')
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
        t = threading.Thread(target=costumer, args=(file, dataQUEUE, lock,))
        parse_threads.append(t)
        t.start()

    for thread in parse_threads:
        thread.join()

    end = time.time()
    print("执行完毕，耗时：", end - start)
    with lock:
        file.close()







