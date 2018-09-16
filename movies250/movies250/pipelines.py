# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from movies250.items import *


class MongoPipeline(object):

	collection1 = "Basic_infos"
	collection2 = "Reviews_detials"

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		"""通过from_crawler类方法获取settings的信息"""
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
			mongo_db=crawler.settings.get('MONGO_DB')
			)

	def open_spider(self, spider):
		"""创建MongoDB的client并连接db"""
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def process_item(self, item, spider):
		"""官方推荐用insert_one()和insert_many,结果返回Result对象"""
		if item == SurfaceItem():
			self.db[self.collection1].insert(dict(item))
			return item
		elif item == CommentItem():
			self.db[self.collection2].insert(dict(item))
			return item

	def close_spider(self, spider):
		self.client.close()


class MoviesPipeline(object):
	"""保存为JSON格式，以保证数据的正确性"""
	def __init__(self):
		self.file1 = open('Basic_infos.json', 'a', encoding='utf-8')
		self.file2 = open('Reviews_detials.json', 'a', encoding='utf-8')

	def process_item(self, item, spider):
		if item.__class__.__name__ == 'SurfaceItem':
			# dump()将非字符串转成json字符串
			jsondata = json.dumps(dict(item), ensure_ascii=False) + ",\n"
			self.file1.write(jsondata)
		else: 
			jsondata = json.dumps(dict(item), ensure_ascii=False) + ",\n"
			self.file2.write(jsondata)
		return item

	def close_spider(self, spider):
		self.file1.close()
		self.file2.close()


