项目名：微信公众号关键字为Python的信息采集

环境：Python3

IDE：PyCharm

库：scrapy_redis, scrapy, redis, flask

项目描述：先对目标网页进行解析，定制抽取规则为翻页和请求详情页，搭建代理池进行动态更换代理保证采集效率。
         
技术实现：动态代理池更换代理；
         flask搭建代理池API；
         scrapy-redis构建分布式爬虫；
         cookies模拟登录
