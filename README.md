# Spiders-by-shimiruri

项目名：Bilibili 2000万用户信息采集

环境：Python3

IDE：PyCharm

库：scrapy_redis, scrapy, redis, flask, requests, re, json, selenium, pillow

项目描述：selenium破解滑动验证码之后获取cookies；
         requests库建立测试程序验证cookies；
         解析目标网站（AJAX类型），构建分布式爬虫；
         存储数据至MongoDB。
         
技术实现：动态代理池更换代理；
         flask搭建代理池API；
         selenium + Webdriver浏览器渲染破解滑动验证码；
         scrapy-redis构建分布式爬虫；
         AJAX逆向工程。

