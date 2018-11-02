from pkg_resources import resource_filename
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from jt.utils.misc import Logger
from time import sleep
from pyquery import PyQuery as pq

LOG = Logger('captured.py')

class Captured(object):

    def __init__(self, url):
        self.__url = url
        self.browser=webdriver.Chrome(executable_path=resource_filename('jt','drive/chromedriver.exe'))
        self.wait = WebDriverWait(self.browser, 5)

    @property
    def url(self):
        try:
            return self.browser.get(self.__url)
        except TimeoutException:
            LOG.error('%s timeout exception!' % self.__url)

#关键字输入框
    def search_bar(self,search_code,search_key):
        key = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,search_code)))
        key.send_keys(search_key)
        sleep(2)

#时间控件
    def date_bar(self,date_code,date_key):
        # start = self.browser.find_element_by_css_selector(date_code).send_keys(date_key)
        # self.browser.switch_to.frame(start)
        # sleep(2)
        date = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,date_code)))
        date.clear()
        date.send_keys(date_key)
        sleep(2)

#下拉菜单非select
    def select_bar(self,select_code,select_key):
        self.browser.find_element_by_css_selector(select_code).click()
        self.browser.find_element_by_css_selector(select_key).click()
        sleep(2)

#点击框
    def click_bar(self,click_code):
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,click_code)))
        submit.click()
        sleep(2)

#获取内容
    def get_products(self):
        html = self.browser.page_source
        doc = pq(html)
        return doc










