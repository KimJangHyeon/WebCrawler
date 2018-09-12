from bs4 import BeautifulSoup

from Commons import Constants
from selenium import webdriver

from Crawler.models import MyUser
from Info.PiazzaInfo import PiazzaInfo

def push_token_entries():
    push_token_arr = []
    for data in MyUser.objects.filter().all():
        push_token_arr.append(data.push_token)
    return push_token_arr

def get_target(target, base, front_str, back_str):
    ret = str(target)[str(target).find(front_str) + len(front_str):]
    return base + str(ret)[: str(ret).find(back_str)]

def get_targets(target, base, front_str, back_str):
    ret = []
    parsed_target = str(target).split(front_str)
    # print(len(parsed_target))
    if len(parsed_target) == 1:
        # print('no contents')
        return ret

    else:
        # print('have conetent\n\n')
        for data in parsed_target:
            ret.append(data.split(back_str)[0])
    ret.pop(0)
    return ret

def piazza_parser(html, infos):
    ret = []
    soup = BeautifulSoup(html, 'html.parser')
    section_list = soup.find_all('div', {'class': 'resources_section'})
    lecture = soup.find('h1', {'style': 'float:none;'})
    lecture = get_target(lecture, '', '">', '</h1>')
    for section in section_list:
        title = get_target(section, '', '<h2>', '</h2>')
        # print(title)
        # sp = BeautifulSoup(section, 'html.parser')
        # contents = sp.find_all('a', {'class':'resource_title'})
        # print("=========section=========")
        contents = get_targets(section, '', 'class="resource resource_row ui-state-default"', '</tr>')
        # print('contents: '+str(len(contents)))
        for content in contents:
            td = content.split('<td')
            name = td[1]
            name = get_target(name, '', '<div class="view title"><a', '</a></div>')
            name = name.split('>')[1]

            date = td[2]
            date = date.split('>')[2]
            date = date.split('<')[0]

            # title = get_target(content, '', '<div class="view title"><a', '</a></div>')
            # date = get_target(content, '', '<div class="view" style="text-align: center; line-height: 2">', '</div>')
            # print(lecture)
            # print(title)
            # print(name)
            # print(date)
            infos.append(PiazzaInfo(lecture, title, name, date))
            # print("====================\n\n")
            ret.append(content)


