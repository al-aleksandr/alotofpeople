#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import requests
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from common import print_all_event, get_html, convert_month_to_digit

url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0+%D0%B0%D1%84%D0%B8%D1%88%D0%B0&ie=utf-8&oe=utf-8'
f_name = 'PalatsSportu_google_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (g)'

def convert_date(date_str, time_str):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    date_formats = '%d %m'
    time_format = '%H:%M'

    # print(date_str)
    # dt2 = datetime(year=2020, month=5, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

    dt = datetime.strptime(date_str.encode('utf-8').strip(), date_formats)
    if dt.month >= datetime.today().month:
        dt = dt.replace(year=datetime.today().year)
    else:
        dt = dt.replace(year=datetime.today().year + 1)

    # print(time_str)
    # if time_str != "--:--":
    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)
    # print(dt)
    return dt

def analize_event(title_in, date_in, time_in):
    dt = convert_date(date_in[4:], time_in)
    print('%70s: %s at %s' % (title_in, dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M")))

def get_events_google(html_file):
    # page = requests.get('https://www.google.com/search?client=ubuntu&channel=fs&q=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0+%D0%B0%D1%84%D0%B8%D1%88%D0%B0&ie=utf-8&oe=utf-8')
    # # tree = html.fromstring(page.content)
    # print(page.encoding)
    # page.encoding = 'cp1251'
    # tree = html.fromstring(page.content)
    # root = html.parse(StringIO(page.text)).getroot()
    # body = root[1]
    event_list = []

    # html_file = open('google_sport.html').read()
    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('div', class_='h998We mlo-c')
    for event_div in events_soup:
        event_date = convert_month_to_digit(event_div.find('div', class_='aXUuyd').text[4:])
        div_time = event_div.find('div', class_='HoEOQb')
        if div_time is None:
            event_time = '00:00'
        else:
            event_time = div_time.text
        event_title = event_div.find('div', class_='title').text
        event_title += event_ending_name
        dt = convert_date(event_date, event_time)
        # print('%70s: %s at %s' % (event_title, dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M")))
        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)
        # analize_event(event_title, event_date, event_time)

    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

# def print_all_event(event_list):
#     for item in event_list:
#         print('%70s: %s at %s' % (item['title'], item['date'].strftime("%d/%m/%Y"), item['date'].strftime("%H:%M")))

def get_events_google_2(html_file):
    # page = requests.get('https://www.google.com/search?client=ubuntu&channel=fs&q=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0+%D0%B0%D1%84%D0%B8%D1%88%D0%B0&ie=utf-8&oe=utf-8')
    # # tree = html.fromstring(page.content)
    # print(page.encoding)
    # page.encoding = 'cp1251'
    # tree = html.fromstring(page.content)
    # root = html.parse(StringIO(page.text)).getroot()
    # body = root[1]
    event_list = []

    # html_file = open('google_sport.html').read()
    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('div', class_='h998We mlo-c')
    for event_div in events_soup:
        event_date = event_div.find('div', class_='aXUuyd').text[4:]
        div_time = event_div.find('div', class_='HoEOQb')
        if div_time is None:
            event_time = '--:--'
        else:
            event_time = div_time.text
        event_title = event_div.find('div', class_='title').text
        dt = convert_date(event_date, event_time)
        # print('%70s: %s at %s' % (event_title, dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M")))
        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)
        # analize_event(event_title, event_date, event_time)
    return event_list

def save_to_file(file_name, str_to_save):
    text_file = open(file_name, "w")
    text_file.write(str_to_save)
    text_file.close()

def get_list():
    global url
    global f_name
    global dt_last_update

    print("PalatsSportu_goole is called")
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_google(html_file)

    return event_list

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
