from scrapy.utils.project import get_project_settings
from steam.utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
	name = 'steam' 
	custom_settings = get_config(name)
	spider = custom_settings.get('spidername')
	
	"""先把project设置字典化，再与json设置更新"""
	project_settings = get_project_settings()
	settings = dict(project_settings.copy())
	settings.update(custom_settings.get('settings'))

	"""传入settings，再启动crawl"""
	process = CrawlerProcess(settings)
	process.crawl(spider, **{'name': name})
	process.start()


if __name__ == '__main__':
	run()


