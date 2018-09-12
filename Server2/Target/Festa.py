import requests
import django
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()
from bs4 import BeautifulSoup
from selenium import webdriver
from Commons import Constants
from Info.FestaInfo import FestaInfo
from Target.Send import send_fcm_notification
from Crawler.models import FestaData, MyUser



def get_url(base, target):
    ret = str(target)[str(target).find('href="/') + 7: str(target).find('">')]
    return base + ret

def flush_festa(new_data):
    for data in new_data:
        FestaData(title=data.title, time=data.time, price=data.price, url=data.url).save()

def push_token_entries():
    push_token_arr = []
    for data in MyUser.objects.filter().all():
        push_token_arr.append(data.push_token)
    return push_token_arr

def parse_festa():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(Constants.DRIVER_PATH, chrome_options=options)
    driver.implicitly_wait(3)
    driver.get(Constants.FESTA)
    festa_data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title_list = soup.select('div > h3')
    time_list = soup.find_all('time')
    price_list = soup.select('a > div > div > span')
    url_list = soup.select('div > div > div > div > div > a')

    for i in range(int(float(len(title_list)/2))):
        festa_info = FestaInfo(title_list[i].text, time_list[i].text, price_list[2 + 3*i].text, get_url(Constants.FESTA, url_list[i + 1]))
        festa_data.append(festa_info)

    return festa_data


def festa_crawler():
    new_data = parse_festa()
    old_data = []
    upload_data = []

    isSame = True
    i = 0
    FestaData_entrys = FestaData.objects.all()

    # data is not null
    if FestaData_entrys.count() != 0:
        #get old data
        for data in FestaData_entrys:
            temp = FestaInfo(data.title, data.time, data.price, data.url)
            old_data.append(temp)

        #check changed
        for data in old_data:
            #is not changed
            if data.url != new_data[i].url or data.title != new_data[i].title:
                FestaData.objects.filter().delete()
                flush_festa(new_data)
                isSame = False
                break
            i += 1

        # entry added
        if not isSame:
            for ndata in new_data:
                isMatch = False
                for odata in old_data:
                    if (odata.url == ndata.url and odata.title == ndata.title):
                        isMatch = True
                        break

                if not isMatch:
                    upload_data.append(ndata)

            for upload in upload_data:
                send_fcm_notification(push_token_entries(), 'festa', upload.title + ' / ' + upload.time)


    #init database(data null)
    else:
        flush_festa(new_data)
