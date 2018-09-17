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


class BiliBili(object):
    """Login bilibili website."""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://passport.bilibili.com/login'
        self.wait = WebDriverWait(self.driver, 10)

    def crack(self, username, password):
        """Crack its captcha
        :param username: Your phonenumber
        :param password: Your password
        :return:
        """
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))

        # This website your must enter your usr and passwd, and it can execute impactfully.
        # Enter your usr.
        user = self.driver.find_element_by_xpath('//input[@id="login-username"]')
        user.clear()
        user.send_keys(username)

        # Enter your passwd.
        passwd = self.driver.find_element_by_xpath('//input[@id="login-passwd"]')
        passwd.clear()
        passwd.send_keys(password)

        # Get two captcha images from login page.
        slider = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).move_to_element(slider).perform()
        time.sleep(1)
        full = self.captchaimage('full.png')
        slider.click()
        time.sleep(3)
        cut = self.captchaimage('cut.png')

        # Calculate the pixel difference between the two pictures to ensure that the distance error is not large.
        distance = self.distance(full, cut)
        
        # Drag slider.
        self.drag(distance)
        try:
            # Decide whether to verify successfully.
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gt_info_tip gt_success"]')))
            print('Login successfully！！！')
            self.driver.quit()
        except TimeoutException:
            print("Failed！Need try again！")
            time.sleep(3)
            return self.drag(distance)

    def captchaimage(self, name):
        """Get captcha images
        :param name: Name of Cropping 
        :return:Image object
        """
        self.driver.get_screenshot_as_file('screen.png')
        screen = Image.open('screen.png')
        element = self.driver.find_element_by_xpath('//div[@class="gt_cut_fullbg gt_show"]')
        location = element.location
        size = element.size
        left, top, right, bottom = location.get('x'), location.get('y'), location.get('x') + size.get('width'), location.get('y') + size.get('height')
        cropimg = screen.crop((left, top, right, bottom))

        # Grayscale conversion, but not necessary
        img = cropimg.convert('L')
        img.save(name)
        return img

    def distance(self, img1, img2):
        """Calculate the pixel difference between the two shots, and find out the distance of the slider moving.
        :param img1: Full img
        :param img2: Gap img
        :return track: Moved distance
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
        """Drag slider and login
        :param distance: Distance of moving slider
        :return:
        """
        element = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        # Subtract the offset from the left side of the slider.
        distance -= 7

        # Start to drag slider
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)

        # Speed up when you drag, then slow down.
        while distance > 0:
            if distance > 10:
                # If distance > 10, move slider faster
                track = random.randint(5, 8)
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
                distance -= track
                # Time is more important!!!
                time.sleep(random.randint(1, 3) / 10)
            else:
                track = random.randint(2, 3)
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
                distance -= track
                # Time is more important!!!
                time.sleep(random.randint(4, 5) / 10 + random.random())
        ActionChains(self.driver).release(on_element=element).perform()


if __name__ == '__main__':
    username = 'your username'
    password = 'your password'
    b_website = BiliBili()
    b_website.crack(username=username, password=password)










