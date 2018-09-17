from bs4 import BeautifulSoup
import os
import sys
import django
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()
from Commons import Constants
import time
from Commons.Constants import PIAZZA_LOGIN, PIAZZA_EMAIL, PIAZZA_PASSWORD
from Crawler.models import PiazzaData
from Target.Parser import get_target, piazza_parser, push_token_entries
from Target.Send import send_fcm_notification

from selenium import webdriver

def flush_data(new_data):
    for data in new_data:
        PiazzaData(lecture=data.lecture, title=data.title, content=data.content, time=data.time).save()

def new_piazza():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(Constants.DRIVER_PATH, chrome_options=options)
    driver.implicitly_wait(3)
    driver.get('https://piazza.com/school-search')
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//button[@class="top-right-button login-hook"]').click()
    driver.find_element_by_name('email').send_keys(PIAZZA_EMAIL)
    driver.find_element_by_name('password').send_keys(PIAZZA_PASSWORD)
    time.sleep(3)
    driver.find_element_by_xpath('//a[@class="primary button"]').click()
    time.sleep(3)
    # driver.implicitly_wait(5)
    driver.find_element_by_xpath('//button[@class="top-right-button dashboardButton classes-hook"]').click()

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    class_list = soup.find_all('li', {'class': 'clearFix classDropdownItem sortable networkDropdown'})

    myclass_url = []
    for myclass in class_list:
        myclass_url.append(get_target(myclass, 'https://piazza.com/class/', "changeNetwork('", "'"))


    piazza_infos=[]
    for data in myclass_url:
        driver.get(data)
        time.sleep(3)
        driver.find_element_by_xpath('//li[@class="top_bar_tab top_bar_course_page"]/a').click()
        time.sleep(3)
        piazza_parser(driver.page_source, piazza_infos)

    return piazza_infos

    # for info in piazza_infos:
    #     print(info.lecture)
    #     print(info.title)
    #     print(info.content)
    #     print(info.time)
    #     print('-----------')

def data_compare(ndata, odata):
    if ndata.lecture == odata.lecture and ndata.content == odata.content:
        return True
    else:
        return False

def piazza_crawler():
    new_datas = new_piazza()
    old_datas = PiazzaData.objects.all()
    upload_datas = []
    if old_datas.count() == 0:
        flush_data(new_datas)
        return

    for ndata in new_datas:
        isNewData = True
        for odata in old_datas:
            if data_compare(ndata, odata):
                isNewData = False
        if isNewData:
            upload_datas.append(ndata)

    if len(upload_datas) != 0:
        flush_data(new_datas)

    for data in upload_datas:
        send_fcm_notification(push_token_entries(), data.lecture, data.title + ' ' + data.content)
        print(data.lecture)
