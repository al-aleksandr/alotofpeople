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

event_ending_name = ' (c)'

def get_html(source=''):
    if source == '':
        url = 'https://concert.ua/ru/search-result?query=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0'
        html_file = get_html_from_internet(url)
    else:
        f_name = 'PalatsSportu_concert_page.txt'
        html_file = get_html_from_file(f_name)

    return html_file

def convert_day_to_normal(date_str):
    # date_str = date_str.replace(u"января", u"Январь")
    # date_str = date_str.replace(u"февраля", u"Февраль")
    # date_str = date_str.replace(u"марта", u"Март")
    # date_str = date_str.replace(u"апреля", u"Апрель")
    # date_str = date_str.replace(u"мая", u"Май")
    # date_str = date_str.replace(u"июня", u"Июнь")
    # date_str = date_str.replace(u"июля", u"Июль")
    # date_str = date_str.replace(u"августа", u"Август")
    # date_str = date_str.replace(u"сентября", u"Сентябрь")
    # date_str = date_str.replace(u"октября", u"Октябрь")
    # date_str = date_str.replace(u"ноября", u"Ноябрь")
    # date_str = date_str.replace(u"декабря", u"Декабрь")

    return date_str

def convert_date(date_str, time_str):
    # print(date_str)
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed
    date_formats = '%d %B'
    time_format = '%H:%M'

    # dt2 = datetime(year=2020, month=3, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

    dt = datetime.strptime(date_str.encode('utf-8').strip(), date_formats)
    if dt.month >= datetime.today().month:
        dt = dt.replace(year=datetime.today().year)
    else:
        dt = dt.replace(year=datetime.today().year + 1)

    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)
    # print(dt)
    return dt

def get_events_concert(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('a', class_='event')
    for event_div in events_soup:
        # print(event_div)
        # return

        event_ar = event_div.find('span', class_='event__date').text.strip()[0:-4]
        event_date = convert_day_to_normal(event_ar[0:-6])
        event_time = event_ar[-6:].strip()
        event_title = event_div.find('span', class_='event__name').text.strip()
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
        # return event_list

    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

def get_list():
    print("PalatsSportu_concert is called")
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed
    html_file = get_html('PalatsSportu_concert_page.txt')
    # html_file = get_html()
    # save_to_file("PalatsSportu_concert_page.txt", html_file)
    event_list = get_events_concert(html_file)
    return event_list

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # the ru locale is installed
    # html_file = get_html()
    # save_to_file("PalatsSportu_concert_page.txt", html_file)
    # event_list = get_events_concert_2(html_file)
    html_file = get_html('PalatsSportu_concert_page.txt')
    # save_to_file("str_from_file.txt", html_file)
    # print(html_file)
    # print(type(html_file))
    # exit()
    event_list = get_events_concert(html_file)
    # print(event_list)
    print_all_event(event_list)
