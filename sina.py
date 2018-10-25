# -*- coding = utf-8 -*-
from requests import Session
from requests.packages import urllib3
import base64
import rsa
import binascii
import time
from urllib.parse import urlencode
import re
import json
import random


class Sina(object):
    """模拟登录新浪微博"""
    def __init__(self, username, passwd):
        self.session = Session()
        self.url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.user = username
        self.passwd = passwd

    def login(self):
        """登录请求
        :param form: POST的表单参数
        :return: 如果成功输出信息，不成功递归本身，重新执行
        """
        response_1 = self.session.post(url=self.url, headers=self.headers, data=self.form(), verify=False).text
        next_url = re.findall('\n\t\tlocation.replace\(\"(.*?)\"\);\n\t\t', response_1, re.S)[0]
        response_2 = self.session.get(next_url, headers=self.headers, verify=False).text
        next_url = re.findall("{location.replace\(\'(.*?)\'\);}", response_2)[0]
        response_3 = self.session.get(next_url, headers=self.headers, verify=False).text
        next_url = re.findall('\"redirect\":\"(.*?)\"', response_3)[0]
        response_4 = self.session.get(next_url.replace('\\', ''), headers=self.headers, verify=False).text
        if '你的用户名' in response_4:
            print('登录成功！')
        else:
            print(response.status_code)

    def form(self):
        """构造POST所需要的表单参数
        :param su, servertime, nonce, rsakv, sp, prelt: 参数均为变化量
        :return: POST参数字典
        """
        params = self.params()
        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '0',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer':'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1540446901.3244',
            'vsbf': '1',
            'su': self.su(),
            'service': 'miniblog',
            'servertime': params.get('servertime'),
            'nonce': params.get('nonce'),
            'pwencode': 'rsa2',
            'rsakv': params.get('rsakv'),
            'sp': self.sp(params),
            'sr': '1600*900',
            'encoding': 'UTF-8',
            'prelt': random.randint(100, 500),
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        return data

    def su(self):
        """对用户名进行base64加密
        :return: 加密完成的字符串
        """
        user = self.user
        s = base64.b64encode(user.encode('utf-8')).decode()
        return s

    def params(self):
        """获取表单所需要的参数
        :return: 包含参数的字典
        """
        query = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.su(),
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.19)',
            '_': int(time.time() * 1000)
        }
        url = 'https://login.sina.com.cn/sso/prelogin.php?' + urlencode(query)
        response = self.session.get(url, headers=self.headers, verify=False).text
        result = json.loads(re.match('sinaSSOController.preloginCallBack\((.*?)\)', response).group(1))
        return result

    def sp(self, params):
        """对密码进行rsa加密
        ":param params: 包含加密所需参数的字典
        :return: 加密完成的字符串
        """
        servertime = params.get('servertime')
        nonce = params.get('nonce')
        pubKey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
        message = str(servertime) + '\t' + str(nonce) + '\n' + self.passwd
        rsa_n = int(pubKey, 16)
        rsa_e = int('10001', 16)
        key = rsa.PublicKey(rsa_n, rsa_e)
        message = rsa.encrypt(message.encode(), key)
        return binascii.b2a_hex(message).decode()


if __name__ == '__main__':
    urllib3.disable_warnings()
    s = Sina('手机号', '登录密码')
    r = s.login()





