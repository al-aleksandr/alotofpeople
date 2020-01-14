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
    # date_str = date_str.replace(u"января,", u"Январь")
    # date_str = date_str.replace(u"февраля,", u"Февраль")
    # date_str = date_str.replace(u"марта,", u"Март")
    # date_str = date_str.replace(u"апреля,", u"Апрель")
    # date_str = date_str.replace(u"мая,", u"Май")
    # date_str = date_str.replace(u"июня,", u"Июнь")
    # date_str = date_str.replace(u"июля,", u"Июль")
    # date_str = date_str.replace(u"августа,", u"Август")
    # date_str = date_str.replace(u"сентября,", u"Сентябрь")
    # date_str = date_str.replace(u"октября,", u"Октябрь")
    # date_str = date_str.replace(u"ноября,", u"Ноябрь")
    # date_str = date_str.replace(u"декабря,", u"Декабрь")

    return date_str

def convert_date(date_str, time_str):
    # print(date_str)
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed

    date_formats = '%d %B, %Y'
    time_format = '%H:%M'

    # dt2 = datetime(year=2020, month=1, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

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
