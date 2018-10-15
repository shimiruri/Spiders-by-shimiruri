# -*- coding=utf-8 -*-
import requests
from requests.packages import urllib3
from queue import Queue
import time
import threading
import json
import pymongo


class CrawlThread(threading.Thread):
	"""Only crawl webpages and save response data to data queue."""
	def __init__(self, pageQueue, dataQueue):
		"""
		:param pageQueue: Save pages of object urls
		:param dataQueue: Save responses from that requests
		:return:
		"""
		super(CrawlThread, self).__init__()
		self.pageQueue = pageQueue
		self.dataQueue = dataQueue
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
		self.url = 'https://www.toutiao.com/search_content/?format=json&keyword=python%E7%88%AC%E8%99%AB&autoload=true&count=20&cur_tab=1&from=search_tab&offset='

	def run(self):
		while True:
			try:
				page = self.pageQueue.get(False)
				url = self.url + str((page - 1) * 20)
				response = requests.get(url, headers=self.headers, verify=False).text
				time.sleep(1)
				self.dataQueue.put(response)
				self.dataQueue.take_done()
			except:
				break
		

class ParseThread(threading.Thread):
	"""Parse responses from data queue and save them to a json file."""
	def __init__(self, file, dataQueue, lock):
		"""
		:param file: File object of saving data
		:param dataQueue: Save responses from that requests
		:param lock: thread lock
		:return:
		"""
		super(ParseThread, self).__init__()
		# self.threadName = threadName
		self.file = file
		self.dataQueue = dataQueue
		self.lock = lock

	def run(self):
		# print("It's time to run " + self.threadName)
		while True:
			try:
				jstring = self.dataQueue.get(False)
				response = json.loads(jstring)
				datas = response.get('data')
				for data in datas:
					title = data.get('title')
					source = data.get('source')
					article_url = data.get('article_url')
					if title is None and source is None and article_url is None:
						pass
					else:
						item = {
							"title": title,
							"source": source,
							"article_url": article_url
						}
						with lock:
							file.write(json.dumps(item, ensure_ascii=False) + ',' + '\n')
			except:
				break


if __name__ == '__main__':
	# Turn off ssl authentication prompt. 
	urllib3.disable_warnings()

	# Define params of threads' class. 
	pageQ = Queue()
	dataQ = Queue()
	file = open('Python spider article.json', 'a', encoding='utf-8')
	lock = threading.Lock()

	# Add page number in urls:
	for i in range(1, 6):
		pageQ.put(i)

	# crawler = ['Crawl-Thread1', 'Crawl-Thread2', 'Crawl-Thread3']
	crawlthreads = []
	for i in range(3):
		crawlthread = CrawlThread(pageQ, dataQ)
		crawlthreads.append(crawlthread)
		crawlthread.start()
	for thread in crawlthreads:
		thread.join()


	# parser = ['Parse-Thread1', 'Parse-Thread2', 'Parse-Thread3']
	parsethreads = []
	for i in range(3):
		parsethread = ParseThread(file, dataQ, lock)
		parsethreads.append(parsethread)
		parsethread.start()
	for thread in parsethreads:
		thread.join()
	
	with lock:
		file.close()
	print('End all!!!')

	

















		
		


		







