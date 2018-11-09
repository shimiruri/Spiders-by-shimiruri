import requests
from requests.packages import urllib3
import json
from cookies import bilibili


def getcookies():
    # bilibili.BiliBili().crack('18722692959', 'wzc5763271430')
    cookies_dict = dict()
    with open("D:/ScrapySpider/bilibili/cookies.txt", 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict


urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'https://space.bilibili.com/4787127/',
    'Connection': 'keep-alive'
}
cookies = getcookies()
form = {
    "mid": "292659952",
    "csrf": cookies.get('bili_jct')
}
print(cookies.get('bili_jct'))
response = requests.post(url='https://space.bilibili.com/ajax/member/GetInfo', data=form, verify=False, cookies=cookies, headers=headers)
print(response.text.encode('utf-8'))

