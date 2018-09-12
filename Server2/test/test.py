from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get('http://www.google.com/xhtml')
