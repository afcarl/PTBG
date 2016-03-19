__author__ = 'luocheng'

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://www.tsinghua.edu.cn')
print browser.page_source
