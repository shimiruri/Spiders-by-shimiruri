# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from PIL import Image
import time
import random
import json


class BiliBili(object):
    """模拟登录B站"""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://passport.bilibili.com/login'
        self.wait = WebDriverWait(self.driver, 10)

    def crack(self, username, password):
        """破解滑动验证码
        :param username: 用户手机号
        :param password: 用户密码
        :return:
        """
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))

        # B站需要先输入用户名和密码，才能有效的执行验证码的滑动
        # 输入用户名
        user = self.driver.find_element_by_xpath('//input[@id="login-username"]')
        user.clear()
        user.send_keys(username)

        # 输入密码
        passwd = self.driver.find_element_by_xpath('//input[@id="login-passwd"]')
        passwd.clear()
        passwd.send_keys(password)

        # 分别获取有缺口和无缺口的两张验证码图片
        slider = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).move_to_element(slider).perform()
        time.sleep(1)
        full = self.captchaimage('full.png')
        slider.click()
        time.sleep(3)
        cut = self.captchaimage('cut.png')

        # 计算两张图片的像素差，确保拖动的距离误差不会很大
        distance = self.distance(full, cut)
        # 拖动滑块
        self.drag(distance)
        try:
            # 判断是否验证成功
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gt_info_tip gt_success"]')))
            print('登陆成功！！！')
            time.sleep(3)
            cookies = self.driver.get_cookies()
            with open('D:/ScrapySpider/bilibili/cookies.txt', 'w') as fp:
                json.dump(cookies, fp)
            self.driver.quit()

        except TimeoutException:
            print("验证失败！重新进行验证！")
            time.sleep(3)
            return self.drag(distance)

    def captchaimage(self, name):
        """获取验证码图片
        :param name: 截图名称
        :return:
        """
        self.driver.get_screenshot_as_file('screen.png')
        screen = Image.open('screen.png')
        element = self.driver.find_element_by_xpath('//div[@class="gt_cut_fullbg gt_show"]')
        location = element.location
        size = element.size
        left, top, right, bottom = location.get('x'), location.get('y'), location.get('x') + size.get('width'), location.get('y') + size.get('height')
        cropimg = screen.crop((left, top, right, bottom))

        # 灰度转换过滤掉小阴影
        img = cropimg.convert('L')
        img.save(name)
        return img

    def distance(self, img1, img2):
        """计算两张截图的像素差，求出滑块移动的距离
        :param img1: 完整的验证码图片
        :param img2: 带缺口的验证码图片
        :return track:    移动距离
        """
        x, y = 60, 1
        track = 0
        while x < img2.width:
            y = 1
            while y < img2.height:
                px1 = img1.getpixel((x, y))
                px2 = img2.getpixel((x, y))
                if abs(px2 - px1) > 50:
                    track = x
                    break
                else:
                    y += 1
            if track:
                break
            x += 1
        return track

    def drag(self, distance):
        """拖动滑块执行登录
        :param distance: 滑块移动距离
        :return:
        """
        element = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        # 除去滑块左边的一点偏移量
        distance -= 7

        # 开始拖动滑块
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)

        # 拖动的时候先加速，再减速
        while distance > 0:
            if distance > 10:
                # If distance > 10, move slider faster
                track = random.randint(5, 8)
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
                distance -= track
                # Time is question!!!
                time.sleep(random.randint(1, 3) / 10)
            else:
                track = random.randint(2, 3)
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
                distance -= track
                # Time is question!!!
                time.sleep(random.randint(4, 5) / 10 + random.random())
        ActionChains(self.driver).release(on_element=element).perform()


if __name__ == '__main__':
    username = '19902051257'
    password = 'wzc5763271430'
    b_website = BiliBili()
    b_website.crack(username=username, password=password)










