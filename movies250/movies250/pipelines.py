# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


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


