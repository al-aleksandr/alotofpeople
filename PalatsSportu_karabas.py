#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from common import print_all_event, get_html_from_file, get_html_from_internet, save_to_file

event_ending_name = ' (k)'

def get_html(source=''):
    if source == '':
        url = 'https://kiev.karabas.com/hall/dvorec-sporta/'
        html_file = get_html_from_internet(url)
    else:
        f_name = 'PalatsSportu_karabas_page.txt'
        html_file = get_html_from_file(f_name)

    return html_file

def convert_day_to_normal(date_str):
    date_str = date_str.lower()
    date_str = date_str.replace(u"января,",   u"01")
    date_str = date_str.replace(u"февраля,",  u"02")
    date_str = date_str.replace(u"марта,",    u"03")
    date_str = date_str.replace(u"апреля,",   u"04")
    date_str = date_str.replace(u"мая,",      u"05")
    date_str = date_str.replace(u"июня,",     u"06")
    date_str = date_str.replace(u"июля,",     u"07")
    date_str = date_str.replace(u"августа,",  u"08")
    date_str = date_str.replace(u"сентября,", u"09")
    date_str = date_str.replace(u"октября,",  u"10")
    date_str = date_str.replace(u"ноября,",   u"11")
    date_str = date_str.replace(u"декабря,",  u"12")

    date_str = date_str.replace(u"январь,",   u"01")
    date_str = date_str.replace(u"февраль,",  u"02")
    date_str = date_str.replace(u"март,",     u"03")
    date_str = date_str.replace(u"апрель,",   u"04")
    date_str = date_str.replace(u"май,",      u"05")
    date_str = date_str.replace(u"июнь,",     u"06")
    date_str = date_str.replace(u"июль,",     u"07")
    date_str = date_str.replace(u"август,",   u"08")
    date_str = date_str.replace(u"сентябрь,", u"09")
    date_str = date_str.replace(u"октябрь,",  u"10")
    date_str = date_str.replace(u"ноябрь,",   u"11")
    date_str = date_str.replace(u"декабрь,",  u"12")

    return date_str

def convert_date(date_str, time_str):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    date_formats = '%d %m %Y'
    time_format = '%H:%M'

    print(date_str)
    dt2 = datetime(year=2020, month=2, day=1)
    print dt2.strftime('We are the %s' %date_formats)

    dt = datetime.strptime(date_str.encode('utf-8').strip(), date_formats)

    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)
    # print(dt)
    return dt

def get_events_karabas(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'html.parser')
    events_soup = soup.find_all('div', class_='ct-table-row ctr-body')
    # print(events_soup)
    for event_div in events_soup:
        # print(event_div)
        # return 
        date_str = event_div.find('ins', class_='ct-date').text[1:4] +\
                event_div.find('ins', class_='ct-date').span.text

        event_date = convert_day_to_normal(date_str)
        event_time = event_div.find_all('span', class_='ctr-cell')[1].find_all('ins')[2].text
        event_title = event_div.find_all('span', class_='ctr-cell')[1].find_all('span', class_='ctr-cell-link')[1].text.strip()
        event_title += event_ending_name

        # print('\n\n\n')
        # print('event_date ---> %s' %(event_date))
        # print('event_time ---> %s' %(event_time))
        # print('event_title ---> %s' %(event_title))

        dt = convert_date(event_date, event_time)
        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)
    
    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )


def get_list():
    print("PalatsSportu_karabas is called")
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed
    html_file = get_html('PalatsSportu_karabas_page.txt')
    # html_file = get_html()
    # save_to_file("PalatsSportu_karabas_page.txt", html_file)
    event_list = get_events_karabas(html_file)
    return event_list

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed
    # html_file = get_html()
    # save_to_file("PalatsSportu_karabas_page.txt", html_file)
    html_file = get_html('PalatsSportu_karabas_page.txt')
    # print(html_file)
    # print(type(html_file))
    # exit()
    event_list = get_events_karabas(html_file)
    # print(event_list)
    print_all_event(event_list)
