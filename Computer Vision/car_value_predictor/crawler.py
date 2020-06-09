import os
import datetime

import cv2
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from utils.two_captcha_wrapper import TwoCaptchaWrapper
from PIL import Image
import time


DRIVER_PATH = '/Users/reysantos7/Desktop/University/University/Computer Vision/car_value_predictor/geckodriver'


class Crawler:
    def __init__(self):
        # options = Options()
        # options.add_argument('-headless')
        self.driver = webdriver.Firefox(executable_path=DRIVER_PATH)
        self.IDS = {
            'license_input': 'search_field',
            'captcha_input': 'code',
            'captcha_img': 'captcha',
        }
        self.XPATHS = {
            'submit_button': '/html/body/div/div[2]/div[1]/div[2]/div[2]/form/div[5]/div/div/a/strong'
        }

    def crawl(self, license_plate: str):
        url = 'https://www.repuve-consulta.com.mx/consulta-ciudadana'

        license_plate = license_plate.replace('-', '').strip()

        self.driver.get(url)

        self.driver.find_element_by_id(
            self.IDS['license_input']).send_keys(license_plate)

        solution = self.solve_captcha()

        self.driver.find_element_by_id(self.IDS['captcha_input']).send_keys(solution)

        self.driver.find_element_by_xpath(self.XPATHS['submit_button']).click()

        html = self.driver.page_source

        self.driver.close()

        return html

    def solve_captcha(self):
        image_name = f'{datetime.datetime.now()}.png'
        captcha_tmp_path = f"captcha_images/{image_name}"
        saved = self.driver.find_element_by_id(self.IDS['captcha_img']).screenshot(captcha_tmp_path)

        if saved:
            im = cv2.imread(captcha_tmp_path)
            # Resize because captcha server doesn't allow images > 100 kb
            im = cv2.resize(im, (140, 90))
            cv2.imwrite(captcha_tmp_path, im)
            # Getting the captcha solution from 2Captcha
            two_captcha = TwoCaptchaWrapper()
            solution = two_captcha.solve_image_captcha(captcha_tmp_path)
            os.remove(captcha_tmp_path)

        return solution
