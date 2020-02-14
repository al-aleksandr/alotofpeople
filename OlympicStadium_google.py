#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import requests
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
from common import print_all_event, get_html, convert_month_to_digit

url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=%D0%BD%D1%81%D0%BA+%D0%BE%D0%BB%D1%96%D0%BC%D0%BF%D1%96%D0%B9%D1%81%D1%8C%D0%BA%D0%B8%D0%B9+%D0%BF%D0%BE%D0%B4%D1%96%D1%97&ie=utf-8&oe=utf-8'
f_name = 'OlympicStatium_google_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (g)'

def convert_date(date_str, time_str):
    date_formats = '%d %m'
    time_format = '%H:%M'

    # print(date_str)
    # dt2 = datetime(year=2020, month=5, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

    if int(date_str[-2:]) >= datetime.today().month:
        dt = datetime(day = int(date_str[:2]), month = int(date_str[-2:]), year=datetime.today().year)
    else:
        dt = datetime(day = int(date_str[:2]), month = int(date_str[-2:]), year=datetime.today().year + 1)

    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)

    return dt

def get_events_google(html_file):
    event_list = []

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

        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)

    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

def get_list():
    global url
    global f_name
    global dt_last_update

    print("OlympicStatium_goole is called")

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_google(html_file)

    return event_list

if __name__ == '__main__':
    # dt_last_update = datetime.today()
    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
